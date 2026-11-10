//! The judge daemon: runs Python submissions in a sandboxed zygote, one job at a time, for the
//! web server, over a Unix socket (protocol in the `openleet-proto` crate).

mod checker;
mod run;
mod watchdog;
mod zygote;

use std::os::unix::fs::PermissionsExt;

use anyhow::{Context, Result};
use openleet_proto::{DEFAULT_SOCKET, Endpoint, Job, Outcome};
use tokio::io::{AsyncBufReadExt, AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt, BufReader};
use tokio::net::{TcpListener, UnixListener};

use crate::zygote::Zygote;

/// Largest job accepted (code plus every test and expected output).
const MAX_JOB_BYTES: usize = 64 << 20;
/// A client has this long to send its job line.
const READ_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(5);
/// No job may ask for more CPU than this, whatever the client says.
const MAX_CPU_LIMIT_MS: u32 = 30_000;
/// The users the zygote runs submissions as (61000 in production, 61001+ in the test builder).
const SANDBOX_UIDS: std::ops::Range<u32> = 61_000..62_000;

struct Config {
    socket: String,
    python: String,
    script: String,
}

impl Config {
    fn from_env() -> Self {
        let var =
            |name: &str, default: &str| std::env::var(name).unwrap_or_else(|_| default.into());
        Self {
            socket: var("JUDGE_SOCKET", DEFAULT_SOCKET),
            python: var("JUDGE_PYTHON", "python3"),
            script: var("JUDGE_ZYGOTE", "/opt/openleet/current/judge/py/zygote.py"),
        }
    }

    async fn zygote(&self) -> Result<Zygote> {
        Zygote::spawn(&self.python, &self.script).await
    }
}

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<()> {
    let config = Config::from_env();
    let endpoint: Endpoint = config.socket.parse()?;
    let listener = Listener::bind(&endpoint).await?;
    let mut zygote = config.zygote().await?;
    eprintln!("judge: listening on {endpoint}");
    // One job at a time: the VM has one core's worth of CPU to give, and timing must be fair.
    loop {
        let (read, write) = listener.accept().await?;
        if !zygote.alive() {
            zygote = config.zygote().await?;
        }
        if let Err(error) = serve(read, write, &mut zygote).await {
            eprintln!("judge: {error:#}");
            zygote = config.zygote().await?;
        }
    }
}

type Reader = Box<dyn AsyncRead + Unpin + Send>;
type Writer = Box<dyn AsyncWrite + Unpin + Send>;

enum Listener {
    Unix(UnixListener),
    Tcp(TcpListener),
}

impl Listener {
    async fn bind(endpoint: &Endpoint) -> Result<Self> {
        Ok(match endpoint {
            Endpoint::Unix(path) => {
                if path.exists() {
                    std::fs::remove_file(path)?;
                }
                let listener = UnixListener::bind(path)
                    .with_context(|| format!("binding {}", path.display()))?;
                // The web server runs as another user.
                std::fs::set_permissions(path, std::fs::Permissions::from_mode(0o666))?;
                Self::Unix(listener)
            }
            Endpoint::Tcp(address) => Self::Tcp(
                TcpListener::bind(address)
                    .await
                    .with_context(|| format!("binding {address}"))?,
            ),
        })
    }

    async fn accept(&self) -> Result<(Reader, Writer)> {
        Ok(match self {
            Self::Unix(listener) => loop {
                let stream = listener.accept().await?.0;
                // The socket is world-writable so the server can reach it; submissions run as
                // sandbox users and must not, or they could queue jobs of their own.
                if stream
                    .peer_cred()
                    .is_ok_and(|peer| !SANDBOX_UIDS.contains(&peer.uid()))
                {
                    let (read, write) = stream.into_split();
                    break (Box::new(read), Box::new(write));
                }
                eprintln!("judge: refused a connection from a sandbox user");
            },
            Self::Tcp(listener) => {
                let (read, write) = listener.accept().await?.0.into_split();
                (Box::new(read), Box::new(write))
            }
        })
    }
}

async fn serve(read: Reader, mut write: Writer, zygote: &mut Zygote) -> Result<()> {
    let mut line = Vec::new();
    let mut reader = BufReader::new(read).take(MAX_JOB_BYTES as u64);
    tokio::time::timeout(READ_TIMEOUT, reader.read_until(b'\n', &mut line))
        .await
        .context("the client sent no job in time")??;
    let outcome = match serde_json::from_slice::<Job>(&line) {
        Ok(mut job) => {
            job.cpu_limit_ms = job.cpu_limit_ms.min(MAX_CPU_LIMIT_MS);
            run::execute(zygote, &job).await?
        }
        Err(error) => Outcome::internal(format!("bad job: {error}")),
    };
    let mut reply = serde_json::to_vec(&outcome)?;
    reply.push(b'\n');
    write.write_all(&reply).await?;
    Ok(())
}
