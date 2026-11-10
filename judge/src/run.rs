//! Runs one [`Job`] through the zygote and turns its events into an [`Outcome`].

use std::time::Duration;

use anyhow::Result;
use openleet_proto::{Case, Expected, Job, Outcome, Verdict};
use serde::Serialize;
use serde_json::Value;
use serde_json::value::RawValue;

use crate::checker::{accepts, digest_matches};
use crate::watchdog::{Kill, KillSwitch, watch};
use crate::zygote::{ChildEvent, Done, Zygote};

/// Virtual memory per solution: the 256 MB recursion stack plus about 400 MB of heap. It sits
/// below the service's 450 MB memory limit, so a memory hog gets a clean MemoryError (Memory
/// Limit Exceeded) before the kernel starts reclaiming memory system-wide, which on a 1 GB
/// machine burns enough CPU to end in a time limit instead.
const ADDRESS_SPACE_MB: u32 = 704;
/// Everything a run may print as answers (big outputs of stress tests fit easily).
const OUTPUT_BYTES: u32 = 64 << 20;
const STDOUT_BYTES: u32 = 16 << 10;

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

/// Longest answer sent back to the server for display; bigger ones are replaced by a note.
const SHOWN_BYTES: usize = 64 << 10;

/// The answer as the server will show it.
fn shown(output: Box<RawValue>) -> Box<RawValue> {
    if output.get().len() <= SHOWN_BYTES {
        return output;
    }
    let note = format!(
        "\"({} KB answer, too large to show)\"",
        output.get().len() >> 10
    );
    RawValue::from_string(note).unwrap_or(output)
}

/// Executes `job`; judge faults come back as [`Verdict::InternalError`], never as `Err`
/// unless the zygote itself broke (the caller then restarts it).
pub async fn execute(zygote: &mut Zygote, job: &Job) -> Result<Outcome> {
    let expected = match job.expected.as_deref().map(parse_expected).transpose() {
        Ok(expected) => expected,
        Err(error) => return Ok(Outcome::internal(format!("bad expected output: {error}"))),
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
        let Some(event) = zygote.next_event().await? else {
            run.garbled();
            continue;
        };
        if let Some(pid) = event.pid {
            run.pid = Some(pid);
            tokio::spawn(watch(
                pid,
                u64::from(job.cpu_limit_ms),
                wall_limit(job.cpu_limit_ms),
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

/// An expected answer, ready to compare.
enum Want<'a> {
    Value(Value),
    Sha256(&'a str),
}

fn parse_expected(expected: &[Expected]) -> serde_json::Result<Vec<Want<'_>>> {
    expected
        .iter()
        .map(|want| match want {
            Expected::Value(raw) => serde_json::from_str(raw.get()).map(Want::Value),
            Expected::Sha256(hex) => Ok(Want::Sha256(hex)),
        })
        .collect()
}

/// A verdict with the test that decided it and the message to show.
type Decision = (Verdict, Option<usize>, Option<String>);

/// State of one job while its events arrive.
struct Run<'a> {
    job: &'a Job,
    expected: Option<Vec<Want<'a>>>,
    cases: Vec<Case>,
    pid: Option<i32>,
    switch: KillSwitch,
    /// The first verdict that is not Accepted.
    settled: Option<Decision>,
}

impl<'a> Run<'a> {
    fn new(job: &'a Job, expected: Option<Vec<Want<'a>>>) -> Self {
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

    /// Whether `out` is right for test `i`; `None` without expected outputs or an answer.
    fn check(&self, i: usize, out: Option<&RawValue>) -> Option<bool> {
        let expected = self.expected.as_ref()?;
        let out = out?.get();
        Some(match expected.get(i) {
            Some(Want::Value(want)) => serde_json::from_str::<Value>(out)
                .is_ok_and(|actual| accepts(self.job.checker, self.job.floats, &actual, want)),
            Some(Want::Sha256(hex)) => digest_matches(out, hex),
            None => false,
        })
    }

    /// The child wrote a line that is no event: the solution wrote to the judge's pipe.
    fn garbled(&mut self) {
        self.settle(
            Verdict::RuntimeError,
            Some(self.cases.len()),
            Some("The program wrote to the judge's pipe".into()),
        );
        self.stop_child();
    }

    fn child_event(&mut self, ev: ChildEvent, cpu_ms: i64) {
        if let Some(message) = ev.compile {
            self.settle(Verdict::CompileError, None, Some(message));
            return;
        }
        if let Some(message) = ev.sandbox {
            self.settle(Verdict::InternalError, None, Some(message));
            return;
        }
        let Some(i) = ev.i else { return };
        // The child keeps running until the kill lands; tests it finishes after the deciding
        // one must not count as passed.
        if self.settled.is_some() && self.job.stop_on_failure {
            return;
        }
        let (output, ok, failure) = if ev.mle == Some(true) {
            (None, None, Some((Verdict::MemoryLimitExceeded, None)))
        } else if let Some(error) = ev.error {
            (None, None, Some((Verdict::RuntimeError, Some(error))))
        } else {
            let ok = self.check(i, ev.out.as_deref());
            let failure = (ok == Some(false)).then_some((Verdict::WrongAnswer, None));
            // A submit only shows its failing case: passing answers are not sent back.
            let keep = !(ok == Some(true) && self.job.stop_on_failure);
            (ev.out.filter(|_| keep).map(shown), ok, failure)
        };
        self.cases.push(Case {
            output,
            stdout: ev.stdout,
            ok,
            cpu_ms: u32::try_from(cpu_ms.max(0)).unwrap_or(u32::MAX),
        });
        if let Some((verdict, error)) = failure {
            self.settle(verdict, Some(i), error);
            if verdict == Verdict::WrongAnswer && self.job.stop_on_failure {
                self.stop_child();
            }
        }
    }

    fn finish(self, done: &Done) -> Outcome {
        let over_time = matches!(self.switch.reason(), Kill::Cpu | Kill::Wall)
            || done.signal == Some(libc::SIGXCPU)
            || done.cpu_ms > self.job.cpu_limit_ms;
        let next_test = Some(self.cases.len());
        // The first judged event decides; then limits, then how the process ended.
        let (verdict, failed, error) = match self.settled {
            Some(settled) => settled,
            None if over_time => (Verdict::TimeLimitExceeded, next_test, None),
            // Killed by the kernel without us asking: the container ran out of memory.
            None if done.signal == Some(libc::SIGKILL) => {
                (Verdict::MemoryLimitExceeded, next_test, None)
            }
            None if done.signal.is_some() || done.code != Some(0) => (
                Verdict::RuntimeError,
                next_test,
                Some(format!("The process ended unexpectedly ({done:?})")),
            ),
            // Judge faults in the child report themselves (`sandbox`); a quiet, clean exit
            // before the last test is the solution's doing (os._exit(0), closing the pipe).
            None if self.cases.len() < self.job.tests.len() => (
                Verdict::RuntimeError,
                next_test,
                Some("The program exited before every test ran".into()),
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

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    /// A job whose `expected` is given in wire form (`[{"value": ..}, {"sha256": ..}]`).
    fn wire_job(tests: usize, expected: &str) -> Job {
        let tests = vec![r#"{"input":{}}"#; tests].join(",");
        serde_json::from_str(&format!(
            r#"{{"spec":{{}},"code":"","tests":[{tests}],"expected":{expected},"cpu_limit_ms":1000,"stop_on_failure":true}}"#
        ))
        .unwrap()
    }

    /// A job expecting the answers in the JSON list `expected`, or only running without it.
    fn job(tests: usize, expected: Option<&str>) -> Job {
        let wire = expected.map_or_else(
            || "null".to_owned(),
            |list| {
                let values: Vec<Value> = serde_json::from_str(list).unwrap();
                let wrapped: Vec<Value> =
                    values.into_iter().map(|v| json!({ "value": v })).collect();
                serde_json::to_string(&wrapped).unwrap()
            },
        );
        wire_job(tests, &wire)
    }

    fn start(job: &Job) -> Run<'_> {
        let expected = job
            .expected
            .as_deref()
            .map(parse_expected)
            .transpose()
            .unwrap();
        Run::new(job, expected)
    }

    fn event(json: &str) -> ChildEvent {
        serde_json::from_str(json).unwrap()
    }

    fn done(json: &str) -> Done {
        serde_json::from_str(json).unwrap()
    }

    const CLEAN: &str = r#"{"code":0,"signal":null,"cpu_ms":40,"maxrss_kb":9000}"#;

    #[test]
    fn all_right_is_accepted() {
        let job = job(2, Some("[1,[2]]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1,"stdout":"hi"}"#), 10);
        run.child_event(event(r#"{"i":1,"out":[2]}"#), 20);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::Accepted);
        assert_eq!(outcome.failed, None);
        assert_eq!(outcome.cases.len(), 2);
        assert_eq!(outcome.cases[0].ok, Some(true));
        assert_eq!(outcome.cases[0].stdout, "hi");
        assert_eq!(outcome.cases[1].cpu_ms, 20);
        assert_eq!((outcome.cpu_ms, outcome.max_rss_kb), (40, 9000));
    }

    #[test]
    fn first_wrong_answer_decides() {
        let job = job(3, Some("[1,2,3]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        run.child_event(event(r#"{"i":1,"out":5}"#), 0);
        run.child_event(event(r#"{"i":2,"error":"boom"}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::WrongAnswer);
        assert_eq!(outcome.failed, Some(1));
        assert_eq!(outcome.error, None);
        assert_eq!(outcome.cases[1].ok, Some(false));
    }

    #[test]
    fn tests_after_the_failure_do_not_count() {
        let job = job(4, Some("[1,2,3,4]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        run.child_event(event(r#"{"i":1,"out":5}"#), 0);
        // The child got further before the kill landed.
        run.child_event(event(r#"{"i":2,"out":3}"#), 0);
        run.child_event(event(r#"{"i":3,"out":4}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::WrongAnswer);
        assert_eq!(outcome.failed, Some(1));
        assert_eq!(outcome.cases.len(), 2);
    }

    #[test]
    fn digest_compares_the_exact_text() {
        // sha256 of `[1,2]`; the second test expects the plain value `[1,2]`.
        let pair = "49a64717d5d4cb19952e6eac2946415cf6879adacf9908e7d872332d32c6e684";
        let job = wire_job(2, &format!(r#"[{{"sha256":"{pair}"}},{{"value":[1,2]}}]"#));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":[1,2]}"#), 0);
        run.child_event(event(r#"{"i":1,"out":[1, 2]}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::Accepted);
        assert_eq!(outcome.cases[0].ok, Some(true));
        assert_eq!(outcome.cases[1].ok, Some(true));

        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":[1, 2]}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::WrongAnswer);
        assert_eq!(outcome.failed, Some(0));
        assert_eq!(
            outcome.cases[0].output.as_deref().map(RawValue::get),
            Some("[1, 2]")
        );
    }

    #[test]
    fn null_answer_is_judged_and_missing_answers_are_not() {
        let job = job(2, Some("[null,1]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":null}"#), 0);
        assert_eq!(run.cases[0].ok, Some(true));
        assert!(run.check(1, None).is_none());
        assert_eq!(
            run.check(5, RawValue::from_string("1".into()).ok().as_deref()),
            Some(false)
        );
    }

    #[test]
    fn without_expected_nothing_is_judged() {
        let job = job(1, None);
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":7}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::Accepted);
        assert_eq!(outcome.cases[0].ok, None);
        assert_eq!(
            outcome.cases[0].output.as_deref().map(RawValue::get),
            Some("7")
        );
    }

    #[test]
    fn runtime_error_and_memory_carry_the_test() {
        let job = job(2, Some("[1,2]"));
        let mut run = start(&job);
        run.child_event(
            event(r#"{"i":0,"error":"ZeroDivisionError","stdout":"x"}"#),
            3,
        );
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::RuntimeError);
        assert_eq!(outcome.failed, Some(0));
        assert_eq!(outcome.error.as_deref(), Some("ZeroDivisionError"));
        assert!(outcome.cases[0].output.is_none());
        assert_eq!(outcome.cases[0].stdout, "x");

        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        run.child_event(event(r#"{"i":1,"mle":true}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::MemoryLimitExceeded);
        assert_eq!(outcome.failed, Some(1));
    }

    #[test]
    fn compile_and_sandbox_errors_have_no_test() {
        let job = job(1, Some("[1]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"compile":"SyntaxError"}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::CompileError);
        assert_eq!(outcome.failed, None);
        assert_eq!(outcome.error.as_deref(), Some("SyntaxError"));

        let mut run = start(&job);
        run.child_event(event(r#"{"sandbox":"OSError"}"#), 0);
        assert_eq!(run.finish(&done(CLEAN)).verdict, Verdict::InternalError);
    }

    #[test]
    fn output_limit_wins_over_the_kill() {
        let job = job(1, Some("[1]"));
        let mut run = start(&job);
        run.settle(Verdict::OutputLimitExceeded, None, None);
        let outcome = run.finish(&done(
            r#"{"code":null,"signal":9,"cpu_ms":5,"maxrss_kb":1}"#,
        ));
        assert_eq!(outcome.verdict, Verdict::OutputLimitExceeded);
    }

    #[test]
    fn time_limit_from_cpu_signal_or_watchdog() {
        let job = job(2, Some("[1,2]"));
        for end in [
            r#"{"code":0,"signal":null,"cpu_ms":1001,"maxrss_kb":1}"#,
            &format!(
                r#"{{"code":null,"signal":{},"cpu_ms":900,"maxrss_kb":1}}"#,
                libc::SIGXCPU
            ),
        ] {
            let mut run = start(&job);
            run.child_event(event(r#"{"i":0,"out":1}"#), 0);
            let outcome = run.finish(&done(end));
            assert_eq!(outcome.verdict, Verdict::TimeLimitExceeded);
            assert_eq!(outcome.failed, Some(1));
        }

        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        assert!(run.switch.claim(Kill::Wall));
        let outcome = run.finish(&done(&format!(
            r#"{{"code":null,"signal":{},"cpu_ms":10,"maxrss_kb":1}}"#,
            libc::SIGKILL
        )));
        assert_eq!(outcome.verdict, Verdict::TimeLimitExceeded);
    }

    #[test]
    fn unasked_kill_is_memory_and_other_ends_are_runtime_errors() {
        let job = job(1, Some("[1]"));
        let killed = format!(
            r#"{{"code":null,"signal":{},"cpu_ms":5,"maxrss_kb":1}}"#,
            libc::SIGKILL
        );
        let outcome = start(&job).finish(&done(&killed));
        assert_eq!(outcome.verdict, Verdict::MemoryLimitExceeded);
        assert_eq!(outcome.failed, Some(0));

        let outcome = start(&job).finish(&done(
            r#"{"code":1,"signal":null,"cpu_ms":5,"maxrss_kb":1}"#,
        ));
        assert_eq!(outcome.verdict, Verdict::RuntimeError);
        assert!(
            outcome
                .error
                .unwrap()
                .starts_with("The process ended unexpectedly")
        );
    }

    #[test]
    fn clean_exit_with_missing_tests_is_a_runtime_error() {
        let job = job(2, Some("[1,2]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::RuntimeError);
        assert_eq!(outcome.failed, Some(1));
    }

    #[test]
    fn writing_to_the_judge_pipe_is_a_runtime_error() {
        let job = job(2, Some("[1,2]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        run.garbled();
        run.child_event(event(r#"{"i":1,"out":2}"#), 0);
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::RuntimeError);
        assert_eq!(outcome.failed, Some(1));
    }

    #[test]
    fn negative_cpu_reads_as_zero() {
        let job = job(1, None);
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), -1);
        assert_eq!(run.cases[0].cpu_ms, 0);
    }

    #[test]
    fn big_answers_are_replaced_by_a_note() {
        let small = RawValue::from_string("[1,2]".to_owned()).unwrap();
        assert_eq!(shown(small).get(), "[1,2]");
        let big = RawValue::from_string(format!("\"{}\"", "x".repeat(SHOWN_BYTES))).unwrap();
        assert_eq!(shown(big).get(), "\"(64 KB answer, too large to show)\"");
    }
}
