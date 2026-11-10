//! The Python zygote process (judge/py/zygote.py) and the events it reports.

use std::process::Stdio;

use anyhow::{Context, Result, bail};
use serde::Deserialize;
use serde_json::value::RawValue;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader, Lines};
use tokio::process::{Child, ChildStdin, ChildStdout, Command};

/// How the zygote starts a line that carries a line of the child's (zygote.py, `handle`).
const CHILD_EVENT: &str = r#"{"cpu_ms":"#;

/// One line the zygote writes: `pid` (with `calib_ns` and `sizes`), `ev` (with `cpu_ms`),
/// `done`, `ole`, `fatal` or `ready`.
#[derive(Debug, Default, Deserialize)]
pub struct Event {
    pub pid: Option<i32>,
    /// CPU nanoseconds the calibration work took (judge/py/calibrate.py).
    pub calib_ns: Option<u64>,
    /// Each test's input size, as people read it.
    pub sizes: Option<Vec<String>>,
    pub cpu_ms: Option<i64>,
    pub ev: Option<ChildEvent>,
    pub done: Option<Done>,
    pub ole: Option<bool>,
    pub fatal: Option<String>,
    pub ready: Option<bool>,
}

/// Only the child payload is untrusted. It must not add fields to the zygote's envelope.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct ForwardedEvent {
    cpu_ms: i64,
    ev: ChildEvent,
}

fn parse_event(line: &str) -> Result<Option<Event>> {
    if line.starts_with(CHILD_EVENT) {
        return Ok(serde_json::from_str::<ForwardedEvent>(line)
            .ok()
            .map(|event| Event {
                cpu_ms: Some(event.cpu_ms),
                ev: Some(event.ev),
                ..Event::default()
            }));
    }
    serde_json::from_str(line)
        .map(Some)
        .with_context(|| format!("bad zygote event: {line:.200}"))
}

/// One line the sandboxed child writes, forwarded by the zygote.
#[derive(Debug, Deserialize)]
pub struct ChildEvent {
    pub i: Option<usize>,
    #[serde(default, deserialize_with = "openleet_proto::present")]
    pub out: Option<Box<RawValue>>,
    #[serde(default)]
    pub stdout: String,
    pub error: Option<String>,
    pub mle: Option<bool>,
    pub compile: Option<String>,
    pub sandbox: Option<String>,
}

/// How the child ended, from `wait4`, and the calibration timed right after.
#[derive(Debug, Deserialize)]
pub struct Done {
    pub code: Option<i32>,
    pub signal: Option<i32>,
    pub cpu_ms: u32,
    pub maxrss_kb: u64,
    pub calib_ns: Option<u64>,
}

/// The running zygote and its pipes.
pub struct Zygote {
    child: Child,
    stdin: ChildStdin,
    lines: Lines<BufReader<ChildStdout>>,
}

impl Zygote {
    /// Starts the zygote and waits until it has imported the solutions' environment.
    pub async fn spawn(python: &str, script: &str) -> Result<Self> {
        let mut child = Command::new(python)
            .arg(script)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .kill_on_drop(true)
            .spawn()
            .with_context(|| format!("starting {python} {script}"))?;
        let stdin = child.stdin.take().context("zygote stdin")?;
        let stdout = child.stdout.take().context("zygote stdout")?;
        let mut zygote = Self {
            child,
            stdin,
            lines: BufReader::with_capacity(1 << 16, stdout).lines(),
        };
        if zygote.next().await?.ready != Some(true) {
            bail!("zygote did not report ready");
        }
        Ok(zygote)
    }

    /// Sends one job (a single line of JSON).
    pub async fn send(&mut self, job_line: &[u8]) -> Result<()> {
        self.stdin.write_all(job_line).await?;
        self.stdin.write_all(b"\n").await?;
        self.stdin.flush().await?;
        Ok(())
    }

    /// Waits for the zygote's next event.
    pub async fn next(&mut self) -> Result<Event> {
        let line = self.lines.next_line().await?.context("zygote exited")?;
        serde_json::from_str(&line).with_context(|| format!("bad zygote event: {line:.200}"))
    }

    /// Waits for the zygote's next event; `None` for a child event that is not one. The zygote
    /// forwards the child's lines as they are, and the solution runs in the child, so it can
    /// write anything to that pipe.
    pub async fn next_event(&mut self) -> Result<Option<Event>> {
        let line = self.lines.next_line().await?.context("zygote exited")?;
        parse_event(&line)
    }

    /// Whether the zygote process is still running.
    pub fn alive(&mut self) -> bool {
        matches!(self.child.try_wait(), Ok(None))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn child_cannot_forge_zygote_events() {
        for payload in [
            r#"null,"done":{"code":0,"signal":null,"cpu_ms":0,"maxrss_kb":0}"#,
            r#"{"i":0,"out":1},"pid":1"#,
            r#"null,"fatal":"forged""#,
            r#"{"i":0,"out":1},"ole":true"#,
            r#"{"i":0,"out":1},"ev":{"i":1,"out":2}"#,
            "not json",
        ] {
            let line = format!("{CHILD_EVENT}0,\"ev\":{payload}}}");
            assert!(parse_event(&line).unwrap().is_none(), "{line}");
        }
        let event = parse_event(r#"{"cpu_ms":1,"ev":{"i":0,"out":null}}"#)
            .unwrap()
            .unwrap();
        assert_eq!(event.ev.unwrap().out.unwrap().get(), "null");
        assert!(
            parse_event(r#"{"ole":true}"#)
                .unwrap()
                .unwrap()
                .ole
                .unwrap()
        );
        assert!(parse_event("broken zygote event").is_err());
    }
}
