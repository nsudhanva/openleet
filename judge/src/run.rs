//! Runs one [`Job`] through the zygote and turns its events into an [`Outcome`].
//!
//! Time is judged in reference milliseconds. Right before each run, and again right after it,
//! the zygote times a fixed piece of work (judge/py/calibrate.py); how much longer that took
//! than on the reference machine is the machine's slowdown. The watchdog allows the job's limit
//! times the slowdown measured before, and CPU times are reported divided by the slowdown over
//! the run, so a busy or throttled machine neither fails a solution nor makes it look slow. A
//! run that hits the limit runs once more when the machine slowed down during it (the e2-micro
//! drops to a seventh of its speed when its burst allowance runs out) or when another run is
//! cheap; a time limit stands only when both runs hit it.

use std::time::Duration;

use anyhow::Result;
use openleet_proto::{Case, Expected, Job, MAX_RUN_CPU_MS, Outcome, Verdict, wall_limit_ms};
use serde::Serialize;
use serde_json::Value;
use serde_json::value::RawValue;

use crate::checker::{accepts, digest_matches};
use crate::watchdog::{Kill, KillSwitch, watch};
use crate::zygote::{ChildEvent, Done, Zygote};

/// Virtual memory per solution: the 256 MB recursion stack plus about 400 MB of heap. It sits
/// below the service's 450 MB memory limit, so a memory hog gets a clean `MemoryError` (Memory
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

/// The calibration work's CPU time on the reference machine (an Apple M1 Pro core running the
/// judge's container): one reference millisecond is a millisecond there.
const REFERENCE_CALIBRATION_NS: f64 = 25_000_000.0;
/// Slowdowns outside this range are measuring faults, not machines.
const SLOWDOWNS: (f64, f64) = (0.2, 100.0);
/// A run that hits the time limit runs again when the machine is this much slower after it
/// than before...
const SLOWER: f64 = 1.25;
/// ...or when running it again costs at most this much of the machine's CPU: a calibration
/// is a moment's sample of a shared core, so one unlucky stretch must not decide a verdict.
const RERUN_MACHINE_MS: u32 = 30_000;

/// How many times longer than on the reference machine the calibration took.
fn slowdown(calib_ns: u64) -> f64 {
    // Calibration times are well below 2^53 ns, so the conversion is exact.
    #[allow(clippy::cast_precision_loss)]
    let ns = calib_ns as f64;
    (ns / REFERENCE_CALIBRATION_NS).clamp(SLOWDOWNS.0, SLOWDOWNS.1)
}

/// CPU milliseconds on the judge's machine as reference milliseconds.
fn reference_ms(machine_ms: f64, slowdown: f64) -> u32 {
    // Non-negative and far below u32::MAX: at most MAX_RUN_CPU_MS / SLOWDOWNS.0.
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    let ms = (machine_ms.max(0.0) / slowdown).round() as u32;
    ms
}

/// Judges `job`, running it a second time when its first run hit the time limit and that run
/// may have been unlucky (see [`Run::worth_rerunning`]); a time limit stands only when both
/// runs hit it.
pub async fn judge(zygote: &mut Zygote, job: &Job) -> Result<Outcome> {
    let (first, worth_rerunning) = execute(zygote, job).await?;
    if first.verdict != Verdict::TimeLimitExceeded || !worth_rerunning {
        return Ok(first);
    }
    let (mut second, _) = execute(zygote, job).await?;
    second.rerun = true;
    Ok(second)
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

/// Executes `job` once, and tells whether a time limit would be worth running again;
/// judge faults come back as [`Verdict::InternalError`], never as `Err` unless the zygote
/// itself broke (the caller then restarts it).
async fn execute(zygote: &mut Zygote, job: &Job) -> Result<(Outcome, bool)> {
    let expected = match job.expected.as_deref().map(parse_expected).transpose() {
        Ok(expected) => expected,
        Err(error) => {
            let outcome = Outcome::internal(format!("bad expected output: {error}"));
            return Ok((outcome, false));
        }
    };
    let line = serde_json::to_vec(&ZygoteJob {
        spec: &job.spec,
        code: &job.code,
        tests: &job.tests,
        limits: Limits {
            // The kernel's backstop, set before the machine's speed is known; the watchdog
            // enforces the real limit to 10 ms.
            cpu_s: MAX_RUN_CPU_MS.div_ceil(1000) + 1,
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
            run.start(pid, event.calib_ns.map_or(1.0, slowdown), event.sizes);
            tokio::spawn(watch(
                pid,
                u64::from(run.machine_limit_ms),
                Duration::from_millis(wall_limit_ms(run.machine_limit_ms)),
                run.switch.clone(),
            ));
        } else if let Some(ev) = event.ev {
            run.child_event(ev, event.cpu_ms.unwrap_or(0));
        } else if event.ole == Some(true) {
            run.settle(Verdict::OutputLimitExceeded, None, None);
        } else if let Some(done) = event.done {
            let again = run.worth_rerunning(&done);
            return Ok((run.finish(&done), again));
        } else if let Some(fatal) = event.fatal {
            return Ok((Outcome::internal(fatal), false));
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
    /// How much slower than the reference machine this machine is right now.
    slowdown: f64,
    /// The CPU the watchdog allows on this machine: the job's limit times the slowdown, but
    /// never more than [`MAX_RUN_CPU_MS`].
    machine_limit_ms: u32,
    /// Whether [`MAX_RUN_CPU_MS`] cut the job's limit (the machine is too slow to give it).
    capped: bool,
    sizes: Vec<String>,
}

impl<'a> Run<'a> {
    fn new(job: &'a Job, expected: Option<Vec<Want<'a>>>) -> Self {
        let mut run = Self {
            job,
            expected,
            cases: Vec::new(),
            pid: None,
            switch: KillSwitch::default(),
            settled: None,
            slowdown: 1.0,
            machine_limit_ms: 0,
            capped: false,
            sizes: Vec::new(),
        };
        run.set_slowdown(1.0);
        run
    }

    fn set_slowdown(&mut self, slowdown: f64) {
        let wanted = f64::from(self.job.cpu_limit_ms) * slowdown;
        self.slowdown = slowdown;
        self.capped = wanted > f64::from(MAX_RUN_CPU_MS);
        // Clamped into u32's range first, so the conversion cannot truncate or wrap.
        #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
        let limit = wanted.min(f64::from(MAX_RUN_CPU_MS)).round() as u32;
        self.machine_limit_ms = limit;
    }

    /// The child started, on a machine `slowdown` times slower than the reference.
    fn start(&mut self, pid: i32, slowdown: f64, sizes: Option<Vec<String>>) {
        self.pid = Some(pid);
        self.set_slowdown(slowdown);
        self.sizes = sizes.unwrap_or_default();
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
        if i != self.cases.len()
            || i >= self.job.tests.len()
            || (ev.out.is_none() && ev.error.is_none() && ev.mle != Some(true))
        {
            self.garbled();
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
        // On this machine until `finish` knows the slowdown over the whole run.
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

    /// The machine's slowdown measured once the child had ended.
    fn after(&self, done: &Done) -> f64 {
        done.calib_ns.map_or(self.slowdown, slowdown)
    }

    /// Whether the machine was [`SLOWER`] after the run than before it.
    fn slowed(&self, done: &Done) -> bool {
        self.after(done) >= self.slowdown * SLOWER
    }

    /// Whether a time limit on this run would be worth running again: the machine slowed
    /// down during it, or another run is cheap ([`RERUN_MACHINE_MS`]).
    fn worth_rerunning(&self, done: &Done) -> bool {
        self.slowed(done) || self.machine_limit_ms <= RERUN_MACHINE_MS
    }

    fn finish(mut self, done: &Done) -> Outcome {
        // The run's slowdown: the mean of before and after, but never below the slowdown its
        // limit was set by, so an accepted run never reports more time than its limit.
        let slowdown = f64::midpoint(self.slowdown, self.after(done)).max(self.slowdown);
        for case in &mut self.cases {
            case.cpu_ms = reference_ms(f64::from(case.cpu_ms), slowdown);
        }
        let over_time = matches!(self.switch.reason(), Kill::Cpu | Kill::Wall)
            || done.signal == Some(libc::SIGXCPU)
            || done.cpu_ms > self.machine_limit_ms;
        let next_test = Some(self.cases.len());
        // The first judged event decides; then limits, then how the process ended.
        let (verdict, failed, error) = match self.settled {
            Some(settled) => settled,
            // Stopped by the judge's own cap before the job's limit: the solution may well be
            // fast enough, the machine is not. Not the solution's fault, so not a verdict on it.
            None if over_time && self.capped => (
                Verdict::InternalError,
                None,
                Some(
                    "The judge's machine is running too slowly right now to give this problem \
                     its full time. Submit again in a few minutes."
                        .into(),
                ),
            ),
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
        let mut cpu_ms = reference_ms(f64::from(done.cpu_ms), slowdown);
        // A run stopped at its limit used all of it, even when the machine slowed down so much
        // that the time it did get comes to less in reference milliseconds.
        if verdict == Verdict::TimeLimitExceeded {
            cpu_ms = cpu_ms.max(self.job.cpu_limit_ms);
        }
        Outcome {
            verdict,
            failed_size: failed.and_then(|i| self.sizes.get(i).cloned()),
            cases: self.cases,
            failed,
            cpu_ms,
            slowdown,
            rerun: false,
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
    fn a_slow_machine_gets_more_cpu_and_reports_reference_time() {
        let job = job(2, Some("[1,2]"));
        let mut run = start(&job);
        run.start(
            7,
            slowdown(75_000_000),
            Some(vec!["n = 1".into(), "n = 9".into()]),
        );
        assert!((run.slowdown - 3.0).abs() < 1e-9);
        assert_eq!(run.machine_limit_ms, 3000);
        run.child_event(event(r#"{"i":0,"out":1}"#), 600);
        // 2.9 s on this machine is under 1 s on the reference machine.
        let end = r#"{"code":null,"signal":9,"cpu_ms":2900,"maxrss_kb":1,"calib_ns":75000000}"#;
        assert!(!run.slowed(&done(end)));
        let outcome = run.finish(&done(end));
        assert_eq!(outcome.verdict, Verdict::MemoryLimitExceeded);
        assert_eq!((outcome.cpu_ms, outcome.cases[0].cpu_ms), (967, 200));
        assert_eq!(outcome.failed_size.as_deref(), Some("n = 9"));

        let mut run = start(&job);
        run.start(7, slowdown(75_000_000), None);
        let outcome = run.finish(&done(
            r#"{"code":0,"signal":null,"cpu_ms":3100,"maxrss_kb":1}"#,
        ));
        assert_eq!(outcome.verdict, Verdict::TimeLimitExceeded);
        assert_eq!(outcome.failed_size, None);
    }

    #[test]
    fn time_is_judged_by_the_slowdown_over_the_run() {
        let job = job(1, Some("[1]"));
        // Slower after the run: it counts as slowed, and a run stopped at its limit reports it.
        let mut run = start(&job);
        run.start(7, 1.0, None);
        let slower = r#"{"code":0,"signal":null,"cpu_ms":1500,"maxrss_kb":1,"calib_ns":75000000}"#;
        assert!(run.slowed(&done(slower)));
        let outcome = run.finish(&done(slower));
        assert_eq!(
            (outcome.verdict, outcome.cpu_ms),
            (Verdict::TimeLimitExceeded, 1000)
        );
        // Faster after it: the slowdown the limit was set by stands.
        let mut run = start(&job);
        run.start(7, 2.0, None);
        run.child_event(event(r#"{"i":0,"out":1}"#), 1500);
        let faster = r#"{"code":0,"signal":null,"cpu_ms":1500,"maxrss_kb":1,"calib_ns":25000000}"#;
        assert!(!run.slowed(&done(faster)));
        let outcome = run.finish(&done(faster));
        assert_eq!((outcome.verdict, outcome.cpu_ms), (Verdict::Accepted, 750));
    }

    #[test]
    fn cheap_or_slowed_runs_are_worth_running_again() {
        let steady =
            done(r#"{"code":0,"signal":null,"cpu_ms":5,"maxrss_kb":1,"calib_ns":25000000}"#);
        let mut job = job(1, Some("[1]"));
        let mut run = start(&job);
        run.start(7, 1.0, None);
        assert!(
            run.worth_rerunning(&steady),
            "a 1 s limit is cheap to run again"
        );
        job.cpu_limit_ms = 60_000;
        let mut run = start(&job);
        run.start(7, 1.0, None);
        assert!(!run.worth_rerunning(&steady));
        let slowed =
            done(r#"{"code":0,"signal":null,"cpu_ms":5,"maxrss_kb":1,"calib_ns":50000000}"#);
        assert!(run.worth_rerunning(&slowed));
    }

    #[test]
    fn the_hard_cap_is_never_a_time_limit_verdict() {
        let mut job = job(1, Some("[1]"));
        job.cpu_limit_ms = MAX_RUN_CPU_MS / 2;
        let mut run = start(&job);
        run.start(7, 4.0, None);
        assert!(run.capped);
        assert_eq!(run.machine_limit_ms, MAX_RUN_CPU_MS);
        assert!(run.switch.claim(Kill::Cpu));
        let outcome = run.finish(&done(CLEAN));
        assert_eq!(outcome.verdict, Verdict::InternalError);
        assert!(outcome.error.unwrap().contains("too slowly"));
    }

    #[test]
    fn slowdowns_are_kept_in_range() {
        assert!((slowdown(25_000_000) - 1.0).abs() < 1e-9);
        assert!((slowdown(0) - SLOWDOWNS.0).abs() < 1e-9);
        assert!((slowdown(u64::MAX) - SLOWDOWNS.1).abs() < 1e-9);
        assert_eq!(reference_ms(-5.0, 2.0), 0);
        assert_eq!(reference_ms(1001.0, 2.0), 501);
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
    fn missing_answers_and_invalid_case_indexes_are_runtime_errors() {
        for forged in [r#"{"i":0}"#, r#"{"i":1,"out":2}"#, r#"{"i":99,"out":1}"#] {
            let job = job(2, Some("[1,2]"));
            let mut run = start(&job);
            run.child_event(event(forged), 0);
            assert_eq!(run.finish(&done(CLEAN)).verdict, Verdict::RuntimeError);
        }
        let job = job(2, Some("[1,2]"));
        let mut run = start(&job);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        run.child_event(event(r#"{"i":0,"out":1}"#), 0);
        assert_eq!(run.finish(&done(CLEAN)).verdict, Verdict::RuntimeError);
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
