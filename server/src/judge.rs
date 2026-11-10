//! Running code: the judge catalog (data/judge/specs.json), the Unix-socket client for the
//! judge daemon, and the Run / Submit flows built on them.

use std::collections::HashMap;
use std::path::Path;
use std::time::{Duration, Instant};

use anyhow::{Context, Result};
use openleet_proto::{
    Checker, Endpoint, Expected, Job, MAX_RUN_CPU_MS, Outcome, Verdict, wall_limit_ms,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use serde_json::value::RawValue;
use tokio::io::{AsyncBufReadExt, AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt, BufReader};
use tokio::net::{TcpStream, UnixStream};
use tokio::sync::Semaphore;

use crate::db::TestRow;
use crate::error::{ApiError, ApiResult};
use openleet::model::Approach;

/// Most jobs that may wait for the judge; more get "busy".
const MAX_WAITING: usize = 4;
/// Largest code accepted anywhere (run, submit, drafts).
pub const MAX_CODE_BYTES: usize = 64 << 10;
/// Largest reply read from the judge daemon.
const MAX_REPLY_BYTES: usize = 16 << 20;
const MAX_CUSTOM_CASES: usize = 10;
/// Longest input or output shown back; bigger ones are cut (stress tests are huge).
const SHOWN_CHARS: usize = 4000;
/// How long a health probe waits to connect to the daemon.
const PROBE_TIMEOUT: Duration = Duration::from_millis(500);
/// How long a probe's answer is reused.
const PROBE_TTL: Duration = Duration::from_secs(5);

/// One problem's entry in specs.json.
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Entry {
    /// Whether the harness can judge it.
    pub supported: bool,
    /// Why it cannot be judged.
    pub reason: Option<String>,
    /// The harness spec, sent with every job.
    pub spec: Option<Box<RawValue>>,
    /// The editor's starting code.
    pub starter: Option<String>,
    #[serde(default)]
    pub checker: Checker,
    #[serde(default)]
    pub floats: bool,
    /// The time limit for all tests together, in reference milliseconds, from the trusted
    /// reference solutions' times (src/openleet/judging/limits.py).
    pub limit_ms: Option<u32>,
    /// A reference solution, which answers custom Run cases.
    pub reference: Option<String>,
    #[serde(default)]
    pub tests: TestCounts,
    /// Parameter names in signature order, from the spec.
    #[serde(skip)]
    pub names: Vec<String>,
    /// Whether it is a design problem (operations and arguments instead of parameters).
    #[serde(skip)]
    pub design: bool,
}

/// How many tests of each kind a problem has.
#[derive(Default, Deserialize, Serialize)]
#[serde(default)]
pub struct TestCounts {
    pub example: u32,
    pub hidden: u32,
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

/// Time limits, in reference milliseconds: the judge measures how fast its machine is during
/// each job and scales them itself, so they hold on any machine under any load.
pub mod limits {
    /// Without a measured limit (specs.json from before the limits were measured).
    pub const DEFAULT_MS: u32 = 2000;
    /// The judge's own cap (it refuses more, whatever the server asks).
    pub const MAX_MS: u32 = 30_000;
    /// Run mode executes only a few small cases.
    pub const RUN_MS: u32 = 5000;
}

impl Entry {
    /// Total CPU time for one submission's tests, in reference milliseconds.
    #[must_use]
    pub fn limit_ms(&self) -> u32 {
        self.limit_ms
            .unwrap_or(limits::DEFAULT_MS)
            .min(limits::MAX_MS)
    }
}

/// The judge catalog and a client for the judge daemon, one job at a time.
pub struct Judge {
    entries: HashMap<String, Entry>,
    endpoint: Endpoint,
    /// One job runs at a time.
    permits: Semaphore,
    /// The running job and the ones waiting: a permit is held for a whole call, so a request
    /// dropped while queued (client gone, HTTP/2 reset, timeout) frees its place.
    queue: Semaphore,
    /// The last health probe: when, and whether the daemon accepted a connection.
    probe: parking_lot::Mutex<Option<(Instant, bool)>>,
}

/// The longest the daemon may take over one job: it runs a job at most twice, each run within
/// its wall-clock limit at the most CPU it ever allows, with a calibration before each.
const JOB_TIMEOUT: Duration = Duration::from_millis(2 * wall_limit_ms(MAX_RUN_CPU_MS) + 60_000);

impl Judge {
    /// Reads specs.json (a missing file means no problem can be judged).
    pub fn load(specs: &Path, endpoint: Endpoint) -> Result<Self> {
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
            queue: Semaphore::new(1 + MAX_WAITING),
            probe: parking_lot::Mutex::new(None),
        })
    }

    /// Whether the daemon accepts a connection (no job is sent; the daemon ignores a
    /// connection that closes without one). Answers are reused for [`PROBE_TTL`].
    pub async fn reachable(&self) -> bool {
        if let Some((at, up)) = *self.probe.lock()
            && at.elapsed() < PROBE_TTL
        {
            return up;
        }
        let connect = async {
            match &self.endpoint {
                Endpoint::Unix(path) => UnixStream::connect(path).await.map(drop),
                Endpoint::Tcp(address) => TcpStream::connect(address).await.map(drop),
            }
        };
        let up = matches!(
            tokio::time::timeout(PROBE_TIMEOUT, connect).await,
            Ok(Ok(()))
        );
        *self.probe.lock() = Some((Instant::now(), up));
        up
    }

    /// A problem's catalog entry.
    pub fn entry(&self, slug: &str) -> Option<&Entry> {
        self.entries.get(slug)
    }

    /// Sends a job to the daemon and waits for its outcome, one job at a time.
    async fn execute(&self, job: &Job) -> ApiResult<Outcome> {
        let _place = self.queue.try_acquire().map_err(|_| ApiError::Busy)?;
        let _turn = self
            .permits
            .acquire()
            .await
            .map_err(|_| ApiError::JudgeDown)?;
        tokio::time::timeout(JOB_TIMEOUT, self.round_trip(job))
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

/// Writes one request line and reads one reply line (at most [`MAX_REPLY_BYTES`]).
async fn exchange(stream: impl AsyncRead + AsyncWrite + Unpin, line: &[u8]) -> Result<Vec<u8>> {
    let (read, mut write) = tokio::io::split(stream);
    write
        .write_all(line)
        .await
        .context("sending the job to the judge")?;
    let mut reply = Vec::new();
    BufReader::new(read.take(MAX_REPLY_BYTES as u64 + 1))
        .read_until(b'\n', &mut reply)
        .await?;
    if reply.len() > MAX_REPLY_BYTES {
        anyhow::bail!("the judge's reply is over {} MiB", MAX_REPLY_BYTES >> 20);
    }
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

/// A JSON value as people read it, cut when long.
pub fn show_value(raw: &str) -> String {
    clip(raw.to_owned())
}

/// An expected output as people read it; big answers are stored only as a checksum.
pub fn show_expected(expected: &Expected) -> String {
    match expected {
        Expected::Value(value) => show_value(value.get()),
        Expected::Sha256(_) => "(large answer, compared by checksum)".to_owned(),
    }
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
            let case = serde_json::json!({ "input": input });
            RawValue::from_string(case.to_string()).map_err(|e| ApiError::Internal(e.into()))
        })
        .collect()
}

/// Input names in display order: the signature's, then any the examples add (such as `pos`).
fn input_names(entry: &Entry, examples: &[TestRow]) -> Vec<String> {
    let mut names = entry.names.clone();
    if let Some(Value::Object(test)) = examples
        .first()
        .and_then(|t| serde_json::from_str(&t.test).ok())
        && let Some(Value::Object(input)) = test.get("input")
    {
        names.extend(input.keys().filter(|k| !entry.names.contains(k)).cloned());
    }
    names
}

/// One case of a Run.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RunCase {
    pub input: String,
    pub output: Option<String>,
    pub expected: Option<String>,
    pub stdout: String,
    pub ok: Option<bool>,
}

/// The result of `POST /api/run`.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct RunResult {
    pub verdict: &'static str,
    pub cases: Vec<RunCase>,
    pub cpu_ms: u32,
    pub error: Option<String>,
}

/// The first failing test of a submission.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Failing {
    pub input: String,
    pub output: Option<String>,
    pub expected: Option<String>,
    pub stdout: String,
    pub kind: String,
    /// How big the test's input is, as "nums: 100,000 items".
    pub size: Option<String>,
}

/// The intended solution's complexity, from the problem's worked approach.
#[derive(Serialize)]
pub struct Complexity {
    pub time: String,
    pub space: String,
}

/// The result of `POST /api/submit`.
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
    /// Shown only with a result: it gives part of the answer away.
    pub intended: Option<Complexity>,
}

/// What a stored submission keeps of its result page (its shape depends on the verdict).
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SubmissionDetail<'a> {
    pub failing: Option<&'a Failing>,
    pub error: Option<&'a str>,
    pub limit_ms: u32,
}

impl SubmitResult {
    /// The part of the result stored with the submission.
    pub fn detail(&self) -> SubmissionDetail<'_> {
        SubmissionDetail {
            failing: self.failing.as_ref(),
            error: self.error.as_deref(),
            limit_ms: self.limit_ms,
        }
    }
}

fn checked_code(code: &str) -> ApiResult<()> {
    if code.trim().is_empty() {
        return Err(ApiError::BadRequest("Write some code first".into()));
    }
    check_code_size(code)
}

/// Rejects code over [`MAX_CODE_BYTES`].
pub fn check_code_size(code: &str) -> ApiResult<()> {
    if code.len() > MAX_CODE_BYTES {
        return Err(ApiError::BadRequest(format!(
            "Code is longer than {} KB",
            MAX_CODE_BYTES >> 10
        )));
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
        let (tests, expected) = if let Some(text) = custom {
            let tests = custom_tests(entry, &input_names(entry, examples), text)?;
            let expected = self
                .reference_answers(entry, &spec, &tests)
                .await?
                .into_iter()
                .map(|answer| answer.map(Expected::Value))
                .collect();
            (tests, expected)
        } else {
            let tests = examples
                .iter()
                .map(|t| raw(&t.test))
                .collect::<ApiResult<Vec<_>>>()?;
            let expected: Vec<Option<Expected>> =
                examples.iter().map(|t| Some(t.expected.clone())).collect();
            (tests, expected)
        };
        let all_known = expected.iter().all(Option::is_some);
        let job = Job {
            spec,
            code: code.to_owned(),
            tests: tests.clone(),
            expected: all_known.then(|| expected.iter().flatten().cloned().collect()),
            checker: entry.checker,
            floats: entry.floats,
            cpu_limit_ms: limits::RUN_MS,
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
                expected: want.as_ref().map(show_expected),
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
            cpu_limit_ms: limits::RUN_MS,
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
        let limit_ms = entry.limit_ms();
        let job = Job {
            spec: spec_of(entry)?,
            code: code.to_owned(),
            tests: tests
                .iter()
                .map(|t| raw(&t.test))
                .collect::<ApiResult<_>>()?,
            expected: Some(tests.iter().map(|t| t.expected.clone()).collect()),
            checker: entry.checker,
            floats: entry.floats,
            cpu_limit_ms: limit_ms,
            stop_on_failure: true,
            capture_stdout: true,
        };
        Ok((self.execute(&job).await?, limit_ms))
    }
}

/// The result page for a submission, from the judge's outcome and the problem's worked
/// approach; `id` is set once stored.
pub fn submit_result(
    entry: &Entry,
    tests: &[TestRow],
    outcome: &Outcome,
    limit_ms: u32,
    approach: Option<&Approach>,
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
            expected: Some(show_expected(&test.expected)),
            stdout: case.map(|c| c.stdout.clone()).unwrap_or_default(),
            kind: test.kind.clone(),
            size: outcome.failed_size.clone(),
        })
    });
    SubmitResult {
        id: 0,
        verdict: outcome.verdict.as_str(),
        passed,
        total,
        cpu_ms: outcome.cpu_ms,
        limit_ms,
        error: outcome.error.clone(),
        failing,
        intended: approach.map(|a| Complexity {
            time: a.time.clone(),
            space: a.space.clone(),
        }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn job() -> Job {
        serde_json::from_str(
            r#"{"spec":{"kind":"function"},"code":"x","tests":[{"input":{}}],"expected":null,"cpu_limit_ms":1000,"stop_on_failure":true}"#,
        )
        .unwrap()
    }

    /// A judge whose daemon accepts connections but never answers.
    async fn silent_judge() -> (Judge, tokio::net::TcpListener) {
        let daemon = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let endpoint = format!("tcp://{}", daemon.local_addr().unwrap());
        let judge = Judge::load(Path::new("missing.json"), endpoint.parse().unwrap()).unwrap();
        (judge, daemon)
    }

    #[tokio::test]
    async fn requests_dropped_while_queued_free_their_place() {
        let (judge, _daemon) = silent_judge().await;
        let job = job();
        let short = Duration::from_millis(50);
        // One job runs (the daemon never answers it).
        let mut running = Box::pin(judge.execute(&job));
        assert!(tokio::time::timeout(short, &mut running).await.is_err());
        // Many more requests than places queue behind it and are given up after a moment, as
        // when a client disconnects: none may leave its place taken.
        for _ in 0..3 * (1 + MAX_WAITING) {
            let outcome = tokio::time::timeout(short, judge.execute(&job)).await;
            assert!(outcome.is_err(), "still waiting, not busy");
        }
        // With every place held, the next request is turned away at once.
        let mut queued: Vec<_> = (0..MAX_WAITING)
            .map(|_| Box::pin(judge.execute(&job)))
            .collect();
        for future in &mut queued {
            assert!(tokio::time::timeout(short, future).await.is_err());
        }
        assert!(matches!(judge.execute(&job).await, Err(ApiError::Busy)));
        drop((queued, running));
        assert!(
            tokio::time::timeout(short, judge.execute(&job))
                .await
                .is_err()
        );
    }

    #[tokio::test]
    async fn refuses_a_reply_over_the_cap() {
        let (client, mut server) = tokio::io::duplex(1 << 16);
        let writer = tokio::spawn(async move {
            let chunk = vec![b'x'; 1 << 16];
            for _ in 0..=(MAX_REPLY_BYTES >> 16) {
                if server.write_all(&chunk).await.is_err() {
                    break;
                }
            }
        });
        let error = exchange(client, b"{}\n").await.unwrap_err();
        assert!(error.to_string().contains("MiB"), "{error:#}");
        writer.abort();
    }
}
