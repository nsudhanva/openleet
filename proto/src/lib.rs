//! Wire types shared by the web server (`cards`) and the judge daemon.
//!
//! One job per Unix-socket connection: the client writes a [`Job`] as one line of JSON, the
//! judge answers with one [`Outcome`] line. Test inputs and outputs travel as raw JSON so the
//! judge forwards them to Python without parsing them.

use serde::{Deserialize, Serialize};
use serde_json::value::RawValue;

/// Where the judge listens by default: systemd's runtime directory for the judge service.
pub const DEFAULT_SOCKET: &str = "/run/google-judge/judge.sock";

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

/// One submission (or reference run) to execute.
#[derive(Debug, Serialize, Deserialize)]
pub struct Job {
    /// The problem's harness spec (see judge/py/harness.py).
    pub spec: Box<RawValue>,
    pub code: String,
    /// Each `{"input": {...}}` or `{"gen": slug, "seed": n, "sha": hex}`.
    pub tests: Vec<Box<RawValue>>,
    /// Expected outputs, one per test; `None` only runs the code (no verdict on answers).
    pub expected: Option<Vec<Box<RawValue>>>,
    #[serde(default)]
    pub checker: Checker,
    /// Compare numbers with LeetCode's 1e-5 tolerance.
    #[serde(default)]
    pub floats: bool,
    /// Total CPU time for all tests together.
    pub cpu_limit_ms: u32,
    /// Stop at the first wrong answer (submit) or run every test (run).
    pub stop_on_failure: bool,
    /// Keep what the code prints (run mode shows it).
    #[serde(default)]
    pub capture_stdout: bool,
}

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
    /// The name the API and the database use.
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
    /// CPU time used up to the end of this test (10 ms resolution).
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
    pub cpu_ms: u32,
    pub max_rss_kb: u64,
    /// Compiler message, traceback, or what went wrong inside the judge.
    pub error: Option<String>,
}

impl Outcome {
    /// An outcome for a job the judge could not run at all.
    #[must_use]
    pub fn internal(error: impl Into<String>) -> Self {
        Self {
            verdict: Verdict::InternalError,
            cases: Vec::new(),
            failed: None,
            cpu_ms: 0,
            max_rss_kb: 0,
            error: Some(error.into()),
        }
    }
}

/// Deserializes a field that may hold JSON `null` as `Some(null)`, so "returned None" and
/// "never answered" (field absent, `None` via `#[serde(default)]`) stay different.
///
/// # Errors
/// Fails when the field is not valid JSON.
pub fn present<'de, D>(deserializer: D) -> Result<Option<Box<RawValue>>, D::Error>
where
    D: serde::Deserializer<'de>,
{
    Box::<RawValue>::deserialize(deserializer).map(Some)
}

/// Where the judge listens: a Unix socket path (production), or `tcp://host:port` for
/// development on machines where the judge runs in a Linux container.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Endpoint {
    Unix(std::path::PathBuf),
    Tcp(String),
}

impl std::str::FromStr for Endpoint {
    type Err = std::convert::Infallible;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        Ok(text.strip_prefix("tcp://").map_or_else(
            || Self::Unix(text.into()),
            |address| Self::Tcp(address.to_owned()),
        ))
    }
}

impl std::fmt::Display for Endpoint {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Unix(path) => write!(f, "{}", path.display()),
            Self::Tcp(address) => write!(f, "tcp://{address}"),
        }
    }
}
