//! Wire types shared by the web server and the judge daemon.
//!
//! One job per Unix-socket connection: the client writes a [`Job`] as one line of JSON, the
//! judge answers with one [`Outcome`] line. Test inputs and outputs travel as raw JSON so the
//! judge forwards them to Python without parsing them.

use std::convert::Infallible;
use std::fmt;
use std::path::PathBuf;
use std::str::FromStr;

use serde::{Deserialize, Serialize};
use serde_json::value::RawValue;

/// Where the judge listens by default: systemd's runtime directory for the judge service.
pub const DEFAULT_SOCKET: &str = "/run/openleet-judge/judge.sock";

/// The most CPU time one run of a job may use on the judge's own machine, however slow that
/// machine is at the moment (a job runs at most twice; see [`Outcome::rerun`]).
pub const MAX_RUN_CPU_MS: u32 = 120_000;

/// The most wall-clock time one run may take: the CPU it may use, twice over, plus a margin.
#[must_use]
pub const fn wall_limit_ms(run_cpu_ms: u32) -> u64 {
    run_cpu_ms as u64 * 2 + 5000
}

/// How an output is compared with the expected one.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Checker {
    /// Same JSON value.
    #[default]
    Exact,
    /// Same list in any order.
    Unordered,
    /// Same list of lists, in any order at both levels.
    UnorderedNested,
}

/// One test's expected answer: `{"value": <json>}` or `{"sha256": "<hex>"}`.
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Expected {
    /// The answer itself, compared with the job's [`Checker`].
    Value(Box<RawValue>),
    /// Lowercase hex SHA-256 of the answer's compact JSON text, for big exact answers. The child
    /// prints answers with that same encoding, so a match means the same answer.
    Sha256(String),
}

/// One submission (or reference run) to execute.
#[derive(Debug, Serialize, Deserialize)]
pub struct Job {
    /// The problem's harness spec (see judge/py/harness.py).
    pub spec: Box<RawValue>,
    pub code: String,
    /// Each `{"input": {...}}` or `{"gen": slug, "seed": n, "sha": hex}`.
    pub tests: Vec<Box<RawValue>>,
    /// Expected outputs, one per test; `None` only runs the code (no verdict on answers).
    pub expected: Option<Vec<Expected>>,
    #[serde(default)]
    pub checker: Checker,
    /// Compare numbers with the official judge's 1e-5 tolerance.
    #[serde(default)]
    pub floats: bool,
    /// Total CPU time for all tests together, in reference milliseconds: what the judge's
    /// calibration says the work would take on its reference machine, however fast or loaded
    /// the judge's own machine is (see judge/py/calibrate.py).
    pub cpu_limit_ms: u32,
    /// Stop at the first wrong answer (submit) or run every test (run).
    pub stop_on_failure: bool,
    /// Keep what the code prints (run mode shows it).
    #[serde(default)]
    pub capture_stdout: bool,
}

/// The judge's ruling on a whole job.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Verdict {
    Accepted,
    WrongAnswer,
    TimeLimitExceeded,
    MemoryLimitExceeded,
    RuntimeError,
    CompileError,
    OutputLimitExceeded,
    InternalError,
}

impl Verdict {
    /// The name the API and the database use (the same as the wire name).
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Accepted => "accepted",
            Self::WrongAnswer => "wrong_answer",
            Self::TimeLimitExceeded => "time_limit_exceeded",
            Self::MemoryLimitExceeded => "memory_limit_exceeded",
            Self::RuntimeError => "runtime_error",
            Self::CompileError => "compile_error",
            Self::OutputLimitExceeded => "output_limit_exceeded",
            Self::InternalError => "internal_error",
        }
    }
}

/// What happened on one test.
#[derive(Debug, Serialize, Deserialize)]
pub struct Case {
    /// The solution's answer, as JSON; absent when it did not finish this test.
    #[serde(
        default,
        deserialize_with = "present",
        skip_serializing_if = "Option::is_none"
    )]
    pub output: Option<Box<RawValue>>,
    #[serde(default, skip_serializing_if = "String::is_empty")]
    pub stdout: String,
    /// Whether the answer matched; `None` without expected outputs or without an answer.
    pub ok: Option<bool>,
    /// CPU time used up to the end of this test, in reference milliseconds (10 ms resolution
    /// on the judge's machine).
    pub cpu_ms: u32,
}

/// The judge's answer to a [`Job`].
#[derive(Debug, Serialize, Deserialize)]
pub struct Outcome {
    pub verdict: Verdict,
    /// Results for the tests that ran, in order.
    pub cases: Vec<Case>,
    /// Index of the test that decided a non-accepted verdict.
    pub failed: Option<usize>,
    /// The size of that test's input, as "nums: 100,000 items, k = 7".
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub failed_size: Option<String>,
    /// CPU time in reference milliseconds (see [`Job::cpu_limit_ms`]).
    pub cpu_ms: u32,
    /// How many times longer than the reference machine the judge's machine took to do the
    /// same work during this job (1 when unknown).
    #[serde(default = "same_speed")]
    pub slowdown: f64,
    /// Whether the job ran twice: its first run hit the time limit while the machine slowed
    /// down, so that run's time said nothing about the solution.
    #[serde(default)]
    pub rerun: bool,
    pub max_rss_kb: u64,
    /// Compiler message, traceback, or what went wrong inside the judge.
    pub error: Option<String>,
}

const fn same_speed() -> f64 {
    1.0
}

impl Outcome {
    /// An outcome for a job the judge could not run at all.
    #[must_use]
    pub fn internal(error: impl Into<String>) -> Self {
        Self {
            verdict: Verdict::InternalError,
            cases: Vec::new(),
            failed: None,
            failed_size: None,
            cpu_ms: 0,
            slowdown: same_speed(),
            rerun: false,
            max_rss_kb: 0,
            error: Some(error.into()),
        }
    }
}

/// Deserializes a field that is there as `Some`, even when it holds JSON `null`; with
/// `#[serde(default)]`, `None` then means left out. So a child's answer `null` ("returned
/// None") stays different from no answer, and a plan's name `null` from no change.
///
/// # Errors
/// Fails when the field's value is not a `T`.
pub fn present<'de, D, T>(deserializer: D) -> Result<Option<T>, D::Error>
where
    D: serde::Deserializer<'de>,
    T: Deserialize<'de>,
{
    T::deserialize(deserializer).map(Some)
}

/// Where the judge listens: a Unix socket path (production), or `tcp://host:port` for
/// development on machines where the judge runs in a Linux container.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Endpoint {
    Unix(PathBuf),
    Tcp(String),
}

impl FromStr for Endpoint {
    type Err = Infallible;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        Ok(text.strip_prefix("tcp://").map_or_else(
            || Self::Unix(text.into()),
            |address| Self::Tcp(address.to_owned()),
        ))
    }
}

impl fmt::Display for Endpoint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Unix(path) => write!(f, "{}", path.display()),
            Self::Tcp(address) => write!(f, "tcp://{address}"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn endpoint_parses_and_displays() {
        let unix: Endpoint = DEFAULT_SOCKET.parse().unwrap();
        assert_eq!(unix, Endpoint::Unix(DEFAULT_SOCKET.into()));
        assert_eq!(unix.to_string(), DEFAULT_SOCKET);

        let tcp: Endpoint = "tcp://127.0.0.1:7777".parse().unwrap();
        assert_eq!(tcp, Endpoint::Tcp("127.0.0.1:7777".into()));
        assert_eq!(tcp.to_string(), "tcp://127.0.0.1:7777");

        let relative: Endpoint = "judge.sock".parse().unwrap();
        assert_eq!(relative, Endpoint::Unix("judge.sock".into()));
    }

    #[test]
    fn verdict_names_match_the_wire() {
        for verdict in [
            Verdict::Accepted,
            Verdict::WrongAnswer,
            Verdict::TimeLimitExceeded,
            Verdict::MemoryLimitExceeded,
            Verdict::RuntimeError,
            Verdict::CompileError,
            Verdict::OutputLimitExceeded,
            Verdict::InternalError,
        ] {
            let wire = serde_json::to_string(&verdict).unwrap();
            assert_eq!(wire, format!("\"{}\"", verdict.as_str()));
        }
    }

    #[test]
    fn job_optional_fields_default() {
        let job: Job = serde_json::from_str(
            r#"{"spec":{"kind":"function"},"code":"x","tests":[{"input":{}}],"expected":null,"cpu_limit_ms":1000,"stop_on_failure":true}"#,
        )
        .unwrap();
        assert_eq!(job.checker, Checker::Exact);
        assert!(!job.floats);
        assert!(!job.capture_stdout);
        assert!(job.expected.is_none());
        assert_eq!(job.tests[0].get(), r#"{"input":{}}"#);
    }

    #[test]
    fn expected_is_externally_tagged() {
        let text = r#"[{"value":{"b":[1, 2.50]}},{"sha256":"ab12"},{"value":null}]"#;
        let expected: Vec<Expected> = serde_json::from_str(text).unwrap();
        let Expected::Value(value) = &expected[0] else {
            panic!("not a value: {expected:?}")
        };
        assert_eq!(value.get(), r#"{"b":[1, 2.50]}"#);
        assert!(matches!(&expected[1], Expected::Sha256(hex) if hex == "ab12"));
        assert!(matches!(&expected[2], Expected::Value(v) if v.get() == "null"));
        assert_eq!(
            serde_json::to_string(&expected).unwrap(),
            r#"[{"value":{"b":[1, 2.50]}},{"sha256":"ab12"},{"value":null}]"#
        );
        assert!(serde_json::from_str::<Expected>("[1]").is_err());
    }

    #[test]
    fn checker_names() {
        let checker: Checker = serde_json::from_str(r#""unordered_nested""#).unwrap();
        assert_eq!(checker, Checker::UnorderedNested);
    }

    #[test]
    fn case_keeps_null_output_apart_from_none() {
        let null: Case = serde_json::from_str(r#"{"output":null,"ok":true,"cpu_ms":5}"#).unwrap();
        assert_eq!(null.output.as_deref().map(RawValue::get), Some("null"));
        let absent: Case = serde_json::from_str(r#"{"ok":null,"cpu_ms":5}"#).unwrap();
        assert!(absent.output.is_none());

        assert_eq!(
            serde_json::to_string(&null).unwrap(),
            r#"{"output":null,"ok":true,"cpu_ms":5}"#
        );
        assert_eq!(
            serde_json::to_string(&absent).unwrap(),
            r#"{"ok":null,"cpu_ms":5}"#
        );
    }

    #[test]
    fn internal_outcome_shape() {
        assert_eq!(
            serde_json::to_string(&Outcome::internal("boom")).unwrap(),
            r#"{"verdict":"internal_error","cases":[],"failed":null,"cpu_ms":0,"slowdown":1.0,"rerun":false,"max_rss_kb":0,"error":"boom"}"#
        );
    }
}
