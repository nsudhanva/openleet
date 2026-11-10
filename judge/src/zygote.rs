//! The Python zygote process (judge/py/zygote.py) and the events it reports.

use std::process::Stdio;

use anyhow::{Context, Result, bail};
use serde::Deserialize;
use serde_json::value::RawValue;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader, Lines};
use tokio::process::{Child, ChildStdin, ChildStdout, Command};

/// One line the zygote writes: `pid`, `ev` (with `cpu_ms`), `done`, `ole`, `fatal` or `ready`.
#[derive(Debug, Deserialize)]
pub struct Event {
    pub pid: Option<i32>,
    pub cpu_ms: Option<i64>,
    pub ev: Option<ChildEvent>,
    pub done: Option<Done>,
    pub ole: Option<bool>,
    pub fatal: Option<String>,
    pub ready: Option<bool>,
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

/// How the child ended, from `wait4`.
#[derive(Debug, Deserialize)]
pub struct Done {
    pub code: Option<i32>,
    pub signal: Option<i32>,
    pub cpu_ms: u32,
    pub maxrss_kb: u64,
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

    /// Whether the zygote process is still running.
    pub fn alive(&mut self) -> bool {
        matches!(self.child.try_wait(), Ok(None))
    }
}
