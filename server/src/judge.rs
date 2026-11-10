//! Running code: the judge catalog (data/judge/specs.json), the Unix-socket client for the
//! judge daemon, and the Run / Submit flows built on them.

use std::collections::HashMap;
use std::path::Path;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;

use anyhow::{Context, Result};
use judge_proto::{Checker, Endpoint, Job, Outcome, Verdict};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use serde_json::value::RawValue;
use tokio::io::{AsyncBufReadExt, AsyncRead, AsyncWrite, AsyncWriteExt, BufReader};
use tokio::net::{TcpStream, UnixStream};
use tokio::sync::Semaphore;

use crate::db::TestRow;
use crate::error::{ApiError, ApiResult};

/// Most jobs that may wait for the judge; more get "busy".
const MAX_WAITING: usize = 4;
const MAX_CODE_BYTES: usize = 64 << 10;
const MAX_CUSTOM_CASES: usize = 10;
/// Longest input or output shown back; bigger ones are cut (stress tests are huge).
const SHOWN_CHARS: usize = 4000;

/// One problem's entry in specs.json.
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Entry {
    pub supported: bool,
    pub reason: Option<String>,
    pub spec: Option<Box<RawValue>>,
    pub starter: Option<String>,
    #[serde(default)]
    pub checker: Checker,
    #[serde(default)]
    pub floats: bool,
    pub ref_cpu_ms: Option<u32>,
    pub slow_cpu_ms: Option<u32>,
    pub reference: Option<String>,
    #[serde(default)]
    pub tests: TestCounts,
    #[serde(skip)]
    pub names: Vec<String>,
    #[serde(skip)]
    pub design: bool,
}

#[derive(Default, Deserialize, Serialize)]
pub struct TestCounts {
    #[serde(default)]
    pub example: u32,
    #[serde(default)]
    pub hidden: u32,
    #[serde(default)]
    pub stress: u32,
}

/// The parts of a harness spec the server reads: kind and parameter names.
#[derive(Deserialize)]
struct SpecShape {
    kind: String,
    #[serde(default)]
    params: Vec<Param>,
}

#[derive(Deserialize)]
struct Param {
    name: String,
}

/// How CPU time on this machine compares with the machine that measured the references
/// (`scale`), and how a problem's limit follows from its references' times.
pub struct TimePolicy {
    pub scale: f64,
}

impl TimePolicy {
    /// A solution may be this many times slower than the fastest reference...
    const FASTEST_FACTOR: f64 = 4.0;
    /// ...and every reference passes: they include submissions LeetCode accepted.
    const SLOWEST_FACTOR: f64 = 1.25;
    const MIN_MS: f64 = 2000.0;
    const MAX_MS: f64 = 20_000.0;
    /// Run mode executes only a few small cases.
    const RUN_MS: u32 = 5000;

    /// Total CPU time for one submission's tests.
    #[must_use]
    pub fn limit_ms(&self, entry: &Entry) -> u32 {
        let fastest = f64::from(entry.ref_cpu_ms.unwrap_or(0)) * Self::FASTEST_FACTOR;
        let slowest = f64::from(entry.slow_cpu_ms.unwrap_or(0)) * Self::SLOWEST_FACTOR;
        let ms = (fastest.max(slowest) * self.scale + 500.0).clamp(Self::MIN_MS, Self::MAX_MS);
        // Clamped to a small positive range, so the conversion cannot truncate or wrap.
        #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
        let ms = ms as u32;
        ms
    }
}

pub struct Judge {
    entries: HashMap<String, Entry>,
    endpoint: Endpoint,
    permits: Semaphore,
    waiting: AtomicUsize,
    pub time: TimePolicy,
}

impl Judge {
    pub fn load(specs: &Path, endpoint: Endpoint, scale: f64) -> Result<Self> {
        let mut entries: HashMap<String, Entry> = if specs.exists() {
            serde_json::from_slice(&std::fs::read(specs)?).context("reading specs.json")?
        } else {
            HashMap::new()
        };
        for entry in entries.values_mut() {
            if let Some(spec) = &mut entry.spec {
                // Jobs travel as single lines, so the pretty-printed file's spacing must go.
                let value: Value = serde_json::from_str(spec.get())?;
                *spec = RawValue::from_string(value.to_string())?;
                let shape: SpecShape = serde_json::from_value(value)?;
                entry.design = shape.kind == "design";
                entry.names = shape.params.into_iter().map(|p| p.name).collect();
            }
        }
        Ok(Self {
            entries,
            endpoint,
            permits: Semaphore::new(1),
            waiting: AtomicUsize::new(0),
            time: TimePolicy { scale },
        })
    }

    pub fn entry(&self, slug: &str) -> Option<&Entry> {
        self.entries.get(slug)
    }

    /// Sends a job to the daemon and waits for its outcome, one job at a time.
    async fn execute(&self, job: &Job) -> ApiResult<Outcome> {
        if self.waiting.fetch_add(1, Ordering::AcqRel) >= MAX_WAITING {
            self.waiting.fetch_sub(1, Ordering::AcqRel);
            return Err(ApiError::Busy);
        }
        let permit = self.permits.acquire().await;
        self.waiting.fetch_sub(1, Ordering::AcqRel);
        let _permit = permit.map_err(|_| ApiError::JudgeDown)?;
        let wall = Duration::from_millis(u64::from(job.cpu_limit_ms) * 6 + 30_000);
        tokio::time::timeout(wall, self.round_trip(job))
            .await
            .map_err(|_| ApiError::JudgeDown)?
            .map_err(|error| {
                tracing::warn!("judge: {error:#}");
                ApiError::JudgeDown
            })
    }

    async fn round_trip(&self, job: &Job) -> Result<Outcome> {
        let mut line = serde_json::to_vec(job)?;
        line.push(b'\n');
        let reply = match &self.endpoint {
            Endpoint::Unix(path) => exchange(UnixStream::connect(path).await?, &line).await?,
            Endpoint::Tcp(address) => exchange(TcpStream::connect(address).await?, &line).await?,
        };
        Ok(serde_json::from_slice(&reply)?)
    }
}

/// Writes one request line and reads one reply line.
async fn exchange(stream: impl AsyncRead + AsyncWrite + Unpin, line: &[u8]) -> Result<Vec<u8>> {
    let (read, mut write) = tokio::io::split(stream);
    write
        .write_all(line)
        .await
        .context("sending the job to the judge")?;
    let mut reply = Vec::new();
    BufReader::new(read).read_until(b'\n', &mut reply).await?;
    Ok(reply)
}

/// A test case as people read it.
#[derive(Serialize)]
pub struct Shown {
    pub input: String,
    pub expected: String,
}

fn clip(mut text: String) -> String {
    if text.chars().count() > SHOWN_CHARS {
        text = text.chars().take(SHOWN_CHARS).collect::<String>() + " …";
    }
    text
}

/// `{"input": {...}}` as LeetCode's "name = value" lines (design problems: two lines).
pub fn show_input(entry: &Entry, test: &str) -> String {
    let Ok(Value::Object(mut wrapper)) = serde_json::from_str::<Value>(test) else {
        return clip(test.to_owned());
    };
    let Some(Value::Object(mut input)) = wrapper.remove("input") else {
        return "(generated stress test)".to_owned();
    };
    if entry.design {
        let ops = input.remove("ops").unwrap_or_default();
        let args = input.remove("args").unwrap_or_default();
        return clip(format!("{ops}\n{args}"));
    }
    let mut lines: Vec<String> = Vec::new();
    for name in &entry.names {
        if let Some(value) = input.remove(name) {
            lines.push(format!("{name} = {value}"));
        }
    }
    lines.extend(
        input
            .into_iter()
            .map(|(name, value)| format!("{name} = {value}")),
    );
    clip(lines.join("\n"))
}

pub fn show_value(raw: &str) -> String {
    clip(raw.to_owned())
}

/// Parses the Testcase box: one JSON value per line, one line per input name, case after case.
fn custom_tests(entry: &Entry, names: &[String], text: &str) -> ApiResult<Vec<Box<RawValue>>> {
    let lines: Vec<&str> = text
        .lines()
        .map(str::trim)
        .filter(|l| !l.is_empty())
        .collect();
    let width = if entry.design { 2 } else { names.len().max(1) };
    if lines.is_empty() || !lines.len().is_multiple_of(width) {
        return Err(ApiError::BadRequest(format!(
            "Each case needs {width} line(s): {}",
            if entry.design {
                "operations, then arguments".to_owned()
            } else {
                names.join(", ")
            }
        )));
    }
    let cases = lines.len() / width;
    if cases > MAX_CUSTOM_CASES {
        return Err(ApiError::BadRequest(format!(
            "At most {MAX_CUSTOM_CASES} cases at a time"
        )));
    }
    let keys: Vec<&str> = if entry.design {
        vec!["ops", "args"]
    } else {
        names.iter().map(String::as_str).collect()
    };
    lines
        .chunks(width)
        .map(|chunk| {
            let mut input = serde_json::Map::new();
            for (key, line) in keys.iter().zip(chunk) {
                let value: Value = serde_json::from_str(line)
                    .map_err(|e| ApiError::BadRequest(format!("{key}: not valid JSON ({e})")))?;
                input.insert((*key).to_owned(), value);
            }
            let test = serde_json::json!({ "input": input });
            RawValue::from_string(test.to_string()).map_err(|e| ApiError::Internal(e.into()))
        })
        .collect()
}

/// Input names in display order: the signature's, then any the examples add (such as `pos`).
fn input_names(entry: &Entry, examples: &[TestRow]) -> Vec<String> {
    let mut names = entry.names.clone();
    if let Some(Value::Object(test)) = examples
        .first()
        .and_then(|t| serde_json::from_str(&t.test).ok())
        && let Some(Value::Object(input)) = test.get("input") {
            names.extend(input.keys().filter(|k| !entry.names.contains(k)).cloned());
        }
    names
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RunCase {
    pub input: String,
    pub output: Option<String>,
    pub expected: Option<String>,
    pub stdout: String,
    pub ok: Option<bool>,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RunResult {
    pub verdict: &'static str,
    pub cases: Vec<RunCase>,
    pub cpu_ms: u32,
    pub error: Option<String>,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Failing {
    pub input: String,
    pub output: Option<String>,
    pub expected: Option<String>,
    pub stdout: String,
    pub kind: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SubmitResult {
    pub id: i64,
    pub verdict: &'static str,
    pub passed: u16,
    pub total: u16,
    pub cpu_ms: u32,
    pub limit_ms: u32,
    pub error: Option<String>,
    pub failing: Option<Failing>,
}

fn checked_code(code: &str) -> ApiResult<()> {
    if code.trim().is_empty() {
        return Err(ApiError::BadRequest("Write some code first".into()));
    }
    if code.len() > MAX_CODE_BYTES {
        return Err(ApiError::BadRequest("Code is longer than 64 KB".into()));
    }
    Ok(())
}

fn spec_of(entry: &Entry) -> ApiResult<Box<RawValue>> {
    entry
        .spec
        .clone()
        .ok_or_else(|| ApiError::BadRequest("This problem cannot be judged yet".into()))
}

fn raw(text: &str) -> ApiResult<Box<RawValue>> {
    RawValue::from_string(text.to_owned()).map_err(|e| ApiError::Internal(e.into()))
}

impl Judge {
    /// Run: the examples (with their known answers) or custom cases (answered by the
    /// reference solution), every case reported, prints included.
    pub async fn run(
        &self,
        entry: &Entry,
        examples: &[TestRow],
        code: &str,
        custom: Option<&str>,
    ) -> ApiResult<RunResult> {
        checked_code(code)?;
        let spec = spec_of(entry)?;
        let (tests, expected) = match custom {
            Some(text) => {
                let tests = custom_tests(entry, &input_names(entry, examples), text)?;
                let expected = self.reference_answers(entry, &spec, &tests).await?;
                (tests, expected)
            }
            None => {
                let tests = examples
                    .iter()
                    .map(|t| raw(&t.test))
                    .collect::<ApiResult<Vec<_>>>()?;
                let expected = examples
                    .iter()
                    .map(|t| raw(&t.expected).map(Some))
                    .collect::<ApiResult<Vec<_>>>()?;
                (tests, expected)
            }
        };
        let all_known = expected.iter().all(Option::is_some);
        let job = Job {
            spec,
            code: code.to_owned(),
            tests: tests.clone(),
            expected: all_known.then(|| expected.iter().flatten().cloned().collect()),
            checker: entry.checker,
            floats: entry.floats,
            cpu_limit_ms: TimePolicy::RUN_MS,
            stop_on_failure: false,
            capture_stdout: true,
        };
        let outcome = self.execute(&job).await?;
        let cases = outcome
            .cases
            .iter()
            .zip(&tests)
            .zip(&expected)
            .map(|((case, test), want)| RunCase {
                input: show_input(entry, test.get()),
                output: case.output.as_ref().map(|o| show_value(o.get())),
                expected: want.as_ref().map(|w| show_value(w.get())),
                stdout: case.stdout.clone(),
                ok: case.ok,
            })
            .collect();
        // Without known answers, finishing is all a run can show.
        let verdict = match outcome.verdict {
            Verdict::Accepted if !all_known => "finished",
            v => v.as_str(),
        };
        Ok(RunResult {
            verdict,
            cases,
            cpu_ms: outcome.cpu_ms,
            error: outcome.error,
        })
    }

    /// The reference solution's answers for custom inputs; `None` where it has none.
    async fn reference_answers(
        &self,
        entry: &Entry,
        spec: &RawValue,
        tests: &[Box<RawValue>],
    ) -> ApiResult<Vec<Option<Box<RawValue>>>> {
        let Some(reference) = &entry.reference else {
            return Ok(vec![None; tests.len()]);
        };
        let job = Job {
            spec: spec.to_owned(),
            code: reference.clone(),
            tests: tests.to_vec(),
            expected: None,
            checker: entry.checker,
            floats: entry.floats,
            cpu_limit_ms: TimePolicy::RUN_MS,
            stop_on_failure: false,
            capture_stdout: false,
        };
        let outcome = self.execute(&job).await?;
        let mut answers: Vec<Option<Box<RawValue>>> =
            outcome.cases.into_iter().map(|c| c.output).collect();
        answers.resize(tests.len(), None);
        Ok(answers)
    }

    /// Submit: every test, stopping at the first failure, against the problem's time limit.
    pub async fn submit(
        &self,
        entry: &Entry,
        tests: &[TestRow],
        code: &str,
    ) -> ApiResult<(Outcome, u32)> {
        checked_code(code)?;
        if tests.is_empty() {
            return Err(ApiError::BadRequest("This problem has no tests yet".into()));
        }
        let limit_ms = self.time.limit_ms(entry);
        let job = Job {
            spec: spec_of(entry)?,
            code: code.to_owned(),
            tests: tests
                .iter()
                .map(|t| raw(&t.test))
                .collect::<ApiResult<_>>()?,
            expected: Some(
                tests
                    .iter()
                    .map(|t| raw(&t.expected))
                    .collect::<ApiResult<_>>()?,
            ),
            checker: entry.checker,
            floats: entry.floats,
            cpu_limit_ms: limit_ms,
            stop_on_failure: true,
            capture_stdout: true,
        };
        Ok((self.execute(&job).await?, limit_ms))
    }
}

/// The result page for a submission, from the judge's outcome.
pub fn submit_result(
    entry: &Entry,
    tests: &[TestRow],
    outcome: &Outcome,
    limit_ms: u32,
    id: i64,
) -> SubmitResult {
    let total = u16::try_from(tests.len()).unwrap_or(u16::MAX);
    let passed = u16::try_from(outcome.cases.iter().filter(|c| c.ok == Some(true)).count())
        .unwrap_or(u16::MAX);
    let failing = outcome.failed.and_then(|i| {
        let test = tests.get(i)?;
        let case = outcome.cases.get(i);
        Some(Failing {
            input: show_input(entry, &test.test),
            output: case
                .and_then(|c| c.output.as_ref())
                .map(|o| show_value(o.get())),
            expected: Some(show_value(&test.expected)),
            stdout: case.map(|c| c.stdout.clone()).unwrap_or_default(),
            kind: test.kind.clone(),
        })
    });
    SubmitResult {
        id,
        verdict: outcome.verdict.as_str(),
        passed,
        total,
        cpu_ms: outcome.cpu_ms,
        limit_ms,
        error: outcome.error.clone(),
        failing,
    }
}
