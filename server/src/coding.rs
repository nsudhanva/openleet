//! The learner's judged submissions, aggregated per problem as they are recorded: counts by
//! verdict, the first verdict, the failures before the first Accepted and when each
//! submission was made. The server replays the stored submissions into a [`CodingLog`] at
//! startup and records each new one, so every read is from memory.

use std::collections::HashMap;

use openleet_proto::Verdict;
use serde::Serialize;

/// Every verdict, in the order [`VerdictCounts`] keeps them.
pub const VERDICTS: [Verdict; 8] = [
    Verdict::Accepted,
    Verdict::WrongAnswer,
    Verdict::TimeLimitExceeded,
    Verdict::MemoryLimitExceeded,
    Verdict::RuntimeError,
    Verdict::CompileError,
    Verdict::OutputLimitExceeded,
    Verdict::InternalError,
];

/// The verdict with this stored name (`Verdict::as_str`).
#[must_use]
pub fn verdict_named(name: &str) -> Option<Verdict> {
    VERDICTS.into_iter().find(|v| v.as_str() == name)
}

/// Whether a verdict is a real failure of the solution, the kind that makes a solve shaky:
/// a wrong answer, a time or memory limit, a crash. A compile error (or an output limit) is
/// a slip, not a misunderstanding, and does not count.
#[must_use]
pub const fn is_failure(verdict: Verdict) -> bool {
    matches!(
        verdict,
        Verdict::WrongAnswer
            | Verdict::TimeLimitExceeded
            | Verdict::MemoryLimitExceeded
            | Verdict::RuntimeError
    )
}

/// Failed submissions this many or more before the first Accepted make a solve shaky.
pub const SHAKY_FAILURES: u32 = 2;

/// How many submissions got each verdict.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct VerdictCounts([u32; VERDICTS.len()]);

impl VerdictCounts {
    fn index(verdict: Verdict) -> usize {
        VERDICTS.iter().position(|&v| v == verdict).unwrap_or(0)
    }

    /// Submissions with this verdict.
    #[must_use]
    pub fn get(&self, verdict: Verdict) -> u32 {
        self.0[Self::index(verdict)]
    }

    fn add(&mut self, verdict: Verdict) {
        self.0[Self::index(verdict)] += 1;
    }

    /// Adds another set of counts.
    pub fn merge(&mut self, other: &Self) {
        for (mine, theirs) in self.0.iter_mut().zip(other.0) {
            *mine += theirs;
        }
    }

    /// The real failures among them (see [`is_failure`]).
    #[must_use]
    pub fn failures(&self) -> u32 {
        VERDICTS
            .into_iter()
            .filter(|&v| is_failure(v))
            .map(|v| self.get(v))
            .sum()
    }
}

/// The failed verdicts as JSON: one count per kind, accepted and internal errors left out.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Failures {
    pub wrong_answer: u32,
    pub time_limit_exceeded: u32,
    pub memory_limit_exceeded: u32,
    pub runtime_error: u32,
    pub compile_error: u32,
    pub output_limit_exceeded: u32,
}

impl From<&VerdictCounts> for Failures {
    fn from(counts: &VerdictCounts) -> Self {
        Self {
            wrong_answer: counts.get(Verdict::WrongAnswer),
            time_limit_exceeded: counts.get(Verdict::TimeLimitExceeded),
            memory_limit_exceeded: counts.get(Verdict::MemoryLimitExceeded),
            runtime_error: counts.get(Verdict::RuntimeError),
            compile_error: counts.get(Verdict::CompileError),
            output_limit_exceeded: counts.get(Verdict::OutputLimitExceeded),
        }
    }
}

/// One problem's submissions, in the order they were judged.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProblemSubmissions {
    /// Every submission, by verdict.
    pub counts: VerdictCounts,
    /// The verdict of the first submission.
    pub first: Verdict,
    /// The submissions before the first Accepted, by verdict (all of them while unsolved).
    pub before_accepted: VerdictCounts,
    /// When the first Accepted came; `None` while unsolved.
    pub accepted_at: Option<i64>,
}

impl ProblemSubmissions {
    fn new(verdict: Verdict) -> Self {
        Self {
            counts: VerdictCounts::default(),
            first: verdict,
            before_accepted: VerdictCounts::default(),
            accepted_at: None,
        }
    }

    fn record(&mut self, verdict: Verdict, at: i64) {
        self.counts.add(verdict);
        if self.accepted_at.is_none() {
            if verdict == Verdict::Accepted {
                self.accepted_at = Some(at);
            } else {
                self.before_accepted.add(verdict);
            }
        }
    }

    /// Whether it has an Accepted submission.
    #[must_use]
    pub const fn solved(&self) -> bool {
        self.accepted_at.is_some()
    }

    /// Whether the first submission was Accepted.
    #[must_use]
    pub fn first_try(&self) -> bool {
        self.first == Verdict::Accepted
    }

    /// Solved, but only after [`SHAKY_FAILURES`] or more real failures, or after any time
    /// limit: worth solving again.
    #[must_use]
    pub fn shaky(&self) -> bool {
        self.solved()
            && (self.before_accepted.failures() >= SHAKY_FAILURES
                || self.before_accepted.get(Verdict::TimeLimitExceeded) > 0)
    }
}

/// Every problem's submissions, and when each submission was made.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct CodingLog {
    problems: HashMap<String, ProblemSubmissions>,
    /// Submission times, Unix milliseconds, in the order recorded.
    times: Vec<i64>,
}

impl CodingLog {
    /// Records a judged submission; calls must come in the order submissions were judged.
    /// Internal errors are the judge's, not the solution's, and are not recorded.
    pub fn record(&mut self, slug: &str, at: i64, verdict: Verdict) {
        if verdict == Verdict::InternalError {
            return;
        }
        self.problems
            .entry(slug.to_owned())
            .or_insert_with(|| ProblemSubmissions::new(verdict))
            .record(verdict, at);
        self.times.push(at);
    }

    /// One problem's submissions.
    #[must_use]
    pub fn problem(&self, slug: &str) -> Option<&ProblemSubmissions> {
        self.problems.get(slug)
    }

    /// Every problem with a submission.
    pub fn problems(&self) -> impl Iterator<Item = (&str, &ProblemSubmissions)> {
        self.problems.iter().map(|(slug, p)| (slug.as_str(), p))
    }

    /// Whether the problem has an Accepted submission.
    #[must_use]
    pub fn solved(&self, slug: &str) -> bool {
        self.problem(slug).is_some_and(ProblemSubmissions::solved)
    }

    /// Whether the problem has any submission.
    #[must_use]
    pub fn tried(&self, slug: &str) -> bool {
        self.problems.contains_key(slug)
    }

    /// Whether the problem's solve is shaky (see [`ProblemSubmissions::shaky`]).
    #[must_use]
    pub fn shaky(&self, slug: &str) -> bool {
        self.problem(slug).is_some_and(ProblemSubmissions::shaky)
    }

    /// When each submission was made.
    #[must_use]
    pub fn times(&self) -> &[i64] {
        &self.times
    }
}

/// A log from solved and merely tried slugs, for tests across modules.
#[cfg(test)]
pub(crate) fn log_of(solved: &[&str], tried: &[&str]) -> CodingLog {
    let mut log = CodingLog::default();
    for slug in tried {
        log.record(slug, 0, Verdict::WrongAnswer);
    }
    for slug in solved {
        log.record(slug, 1, Verdict::Accepted);
    }
    log
}

#[cfg(test)]
mod tests {
    use super::*;

    fn replay(verdicts: &[Verdict]) -> CodingLog {
        let mut log = CodingLog::default();
        for (at, &v) in (0_i64..).zip(verdicts) {
            log.record("p", at, v);
        }
        log
    }

    #[test]
    fn counts_verdicts_and_what_came_before_the_first_accepted() {
        use Verdict::*;
        let log = replay(&[CompileError, WrongAnswer, Accepted, WrongAnswer, Accepted]);
        let p = log.problem("p").expect("recorded");
        assert_eq!((p.first, p.accepted_at), (CompileError, Some(2)));
        assert_eq!(p.counts.get(WrongAnswer), 2);
        assert_eq!(p.counts.get(Accepted), 2);
        assert_eq!(p.before_accepted.get(WrongAnswer), 1);
        assert_eq!(p.before_accepted.get(CompileError), 1);
        assert!(!p.first_try());
        assert_eq!(log.times(), [0, 1, 2, 3, 4]);
        assert!(log.solved("p") && log.tried("p") && !log.tried("q"));
    }

    #[test]
    fn shaky_takes_two_real_failures_or_any_time_limit() {
        use Verdict::*;
        let shaky = |v: &[Verdict]| replay(v).shaky("p");
        assert!(!shaky(&[Accepted]));
        assert!(!shaky(&[WrongAnswer, Accepted]));
        assert!(shaky(&[WrongAnswer, RuntimeError, Accepted]));
        assert!(shaky(&[MemoryLimitExceeded, WrongAnswer, Accepted]));
        // Compile errors (and output limits) do not count.
        assert!(!shaky(&[CompileError, CompileError, WrongAnswer, Accepted]));
        assert!(!shaky(&[OutputLimitExceeded, WrongAnswer, Accepted]));
        // One time limit is enough.
        assert!(shaky(&[TimeLimitExceeded, Accepted]));
        // Failures after the first Accepted do not make it shaky, and unsolved is not shaky.
        assert!(!shaky(&[Accepted, WrongAnswer, TimeLimitExceeded]));
        assert!(!shaky(&[WrongAnswer, WrongAnswer, TimeLimitExceeded]));
    }

    #[test]
    fn leaves_out_the_judges_own_errors() {
        let log = replay(&[Verdict::InternalError, Verdict::Accepted]);
        assert!(log.problem("p").expect("recorded").first_try());
        assert_eq!(log.times().len(), 1);
    }

    #[test]
    fn names_verdicts_and_sorts_failures_into_kinds() {
        for v in VERDICTS {
            assert_eq!(verdict_named(v.as_str()), Some(v));
        }
        assert_eq!(verdict_named("nope"), None);
        let log = replay(&[
            Verdict::WrongAnswer,
            Verdict::CompileError,
            Verdict::TimeLimitExceeded,
        ]);
        let failures = Failures::from(&log.problem("p").expect("recorded").counts);
        assert_eq!(
            (
                failures.wrong_answer,
                failures.compile_error,
                failures.time_limit_exceeded
            ),
            (1, 1, 1)
        );
    }
}
