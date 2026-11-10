//! Runs one [`Job`] through the zygote and turns its events into an [`Outcome`].

use std::time::Duration;

use anyhow::Result;
use judge_proto::{Case, Job, Outcome, Verdict};
use serde::Serialize;
use serde_json::Value;
use serde_json::value::RawValue;

use crate::checker::accepts;
use crate::watchdog::{Kill, KillSwitch, watch};
use crate::zygote::{ChildEvent, Done, Zygote};

/// Virtual memory per solution: room for the 256 MB recursion stack and a big heap. The
/// container's memory limit bounds what is actually resident.
const ADDRESS_SPACE_MB: u32 = 1536;
/// Everything a run may print as answers (big outputs of stress tests fit easily).
const OUTPUT_BYTES: u32 = 64 << 20;
const STDOUT_BYTES: u32 = 16 << 10;
const SIGXCPU: i32 = 24;
const SIGKILL: i32 = 9;

/// The zygote's job line: the parts of a [`Job`] the child needs, never the expected outputs.
#[derive(Serialize)]
struct ZygoteJob<'a> {
    spec: &'a RawValue,
    code: &'a str,
    tests: &'a [Box<RawValue>],
    limits: Limits,
}

#[derive(Serialize)]
struct Limits {
    cpu_s: u32,
    as_mb: u32,
    out_bytes: u32,
    stdout_bytes: u32,
}

/// Wall-clock allowance: generous, since the VM's CPU may be throttled, but bounded.
fn wall_limit(cpu_limit_ms: u32) -> Duration {
    Duration::from_millis(u64::from(cpu_limit_ms) * 4 + 3000)
}

/// Executes `job`; judge faults come back as [`Verdict::InternalError`], never as `Err`
/// unless the zygote itself broke (the caller then restarts it).
pub async fn execute(zygote: &mut Zygote, job: &Job) -> Result<Outcome> {
    let expected: Option<Vec<Value>> = match &job.expected {
        Some(raw) => match raw.iter().map(|r| serde_json::from_str(r.get())).collect() {
            Ok(values) => Some(values),
            Err(error) => return Ok(Outcome::internal(format!("bad expected output: {error}"))),
        },
        None => None,
    };
    let line = serde_json::to_vec(&ZygoteJob {
        spec: &job.spec,
        code: &job.code,
        tests: &job.tests,
        limits: Limits {
            // The kernel's backstop; the watchdog enforces the real limit to 10 ms.
            cpu_s: job.cpu_limit_ms.div_ceil(1000) + 1,
            as_mb: ADDRESS_SPACE_MB,
            out_bytes: OUTPUT_BYTES,
            stdout_bytes: if job.capture_stdout { STDOUT_BYTES } else { 0 },
        },
    })?;
    zygote.send(&line).await?;

    let mut run = Run::new(job, expected);
    loop {
        let event = zygote.next().await?;
        if let Some(pid) = event.pid {
            run.pid = Some(pid);
            let wall = wall_limit(job.cpu_limit_ms);
            tokio::spawn(watch(
                pid,
                u64::from(job.cpu_limit_ms),
                wall,
                run.switch.clone(),
            ));
        } else if let Some(ev) = event.ev {
            run.child_event(ev, event.cpu_ms.unwrap_or(0));
        } else if event.ole == Some(true) {
            run.settle(Verdict::OutputLimitExceeded, None, None);
        } else if let Some(done) = event.done {
            return Ok(run.finish(&done));
        } else if let Some(fatal) = event.fatal {
            return Ok(Outcome::internal(fatal));
        }
    }
}

/// State of one job while its events arrive.
struct Run<'a> {
    job: &'a Job,
    expected: Option<Vec<Value>>,
    cases: Vec<Case>,
    pid: Option<i32>,
    switch: KillSwitch,
    /// The first verdict that is not Accepted, with the test it came from.
    settled: Option<(Verdict, Option<usize>, Option<String>)>,
}

impl<'a> Run<'a> {
    fn new(job: &'a Job, expected: Option<Vec<Value>>) -> Self {
        Self {
            job,
            expected,
            cases: Vec::new(),
            pid: None,
            switch: KillSwitch::default(),
            settled: None,
        }
    }

    fn settle(&mut self, verdict: Verdict, test: Option<usize>, error: Option<String>) {
        self.settled.get_or_insert((verdict, test, error));
    }

    fn stop_child(&self) {
        if let Some(pid) = self.pid {
            self.switch.kill(pid, Kill::Early);
        }
    }

    fn child_event(&mut self, ev: ChildEvent, cpu_ms: i64) {
        let cpu_ms = u32::try_from(cpu_ms.max(0)).unwrap_or(u32::MAX);
        if let Some(message) = ev.compile {
            self.settle(Verdict::CompileError, None, Some(message));
            return;
        }
        if let Some(message) = ev.sandbox {
            self.settle(Verdict::InternalError, None, Some(message));
            return;
        }
        let Some(i) = ev.i else { return };
        if ev.mle == Some(true) {
            self.cases.push(Case {
                output: None,
                stdout: ev.stdout,
                ok: None,
                cpu_ms,
            });
            self.settle(Verdict::MemoryLimitExceeded, Some(i), None);
            return;
        }
        if let Some(error) = ev.error {
            self.cases.push(Case {
                output: None,
                stdout: ev.stdout,
                ok: None,
                cpu_ms,
            });
            self.settle(Verdict::RuntimeError, Some(i), Some(error));
            return;
        }
        let ok = match (&self.expected, &ev.out) {
            (Some(expected), Some(out)) => Some(
                serde_json::from_str::<Value>(out.get()).is_ok_and(|actual| {
                    expected.get(i).is_some_and(|want| {
                        accepts(self.job.checker, self.job.floats, &actual, want)
                    })
                }),
            ),
            _ => None,
        };
        self.cases.push(Case {
            output: ev.out,
            stdout: ev.stdout,
            ok,
            cpu_ms,
        });
        if ok == Some(false) {
            self.settle(Verdict::WrongAnswer, Some(i), None);
            if self.job.stop_on_failure {
                self.stop_child();
            }
        }
    }

    fn finish(self, done: &Done) -> Outcome {
        let over_time = matches!(self.switch.reason(), Kill::Cpu | Kill::Wall)
            || done.signal == Some(SIGXCPU)
            || done.cpu_ms > self.job.cpu_limit_ms;
        let next_test = Some(self.cases.len());
        // The first judged event decides; then limits, then how the process ended.
        let (verdict, failed, error) = match self.settled {
            Some(settled) => settled,
            None if over_time => (Verdict::TimeLimitExceeded, next_test, None),
            // Killed by the kernel without us asking: the container ran out of memory.
            None if done.signal == Some(SIGKILL) => (Verdict::MemoryLimitExceeded, next_test, None),
            None if done.signal.is_some() || done.code != Some(0) => (
                Verdict::RuntimeError,
                next_test,
                Some(format!("The process ended unexpectedly ({done:?})")),
            ),
            None if self.cases.len() < self.job.tests.len() => (
                Verdict::InternalError,
                next_test,
                Some("The run ended before every test ran".into()),
            ),
            None => (Verdict::Accepted, None, None),
        };
        Outcome {
            verdict,
            cases: self.cases,
            failed,
            cpu_ms: done.cpu_ms,
            max_rss_kb: done.maxrss_kb,
            error,
        }
    }
}
