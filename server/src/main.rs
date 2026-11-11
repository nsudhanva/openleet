//! The OpenLeet server: flashcards and coding practice. JSON API, embedded web app, and
//! automatic HTTPS.

mod acme;
mod api;
mod assets;
#[cfg(test)]
mod csp;
mod db;
mod deploy;
mod error;
mod health;
mod judge;
mod listen;
mod preload;
mod security;
mod state;

use std::net::{Ipv6Addr, SocketAddr};
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::time::Duration;

use anyhow::{Context, Result};
use axum::Router;
use axum::extract::{Request, State};
use axum::http::uri::Authority;
use axum::http::{Uri, header};
use axum::middleware::Next;
use axum::response::{IntoResponse, Redirect, Response};
use parking_lot::RwLock;
use rustls_acme::AcmeConfig;

use tower_http::CompressionLevel;
use tower_http::compression::CompressionLayer;

use openleet::content::Content;

use crate::acme::{CertificateSlot, ObservedCache};
use crate::db::{Opening, Store};
use crate::deploy::Deploy;
use crate::judge::Judge;
use crate::listen::Sockets;
use crate::state::{AppState, Progress, Shared};

#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

/// How often cached reports are dropped even without new practice, so the progress page sees
/// cards fall overdue and days pass; the database is checkpointed at the same time.
const REPORT_REFRESH: Duration = Duration::from_mins(15);
/// How often the server checks that the current UTC day has a backup (taken at startup, then
/// once a day; a failed one is retried at the next check).
const BACKUP_CHECK: Duration = Duration::from_hours(1);
/// How long a stopping server waits for in-flight HTTPS requests before closing their
/// connections. Well under `TimeoutStopSec=` in deploy/openleet.service, so systemd never has to
/// kill it: browsers keep idle HTTP/2 connections open, and a drain waits out its whole limit.
const DRAIN: Duration = Duration::from_secs(5);

struct Config {
    data_dir: PathBuf,
    state_dir: PathBuf,
    /// The problems file; `PROBLEMS_FILE`, else `DATA_DIR/problems.json`.
    problems: PathBuf,
    /// `http://host` serves plain HTTP; bare domains (comma-separated) get one HTTPS
    /// certificate, and every domain after the first redirects to the first.
    site: String,
    http_port: u16,
    https_port: u16,
    judge: openleet_proto::Endpoint,
    /// Enables `POST /api/deploy`.
    deploy_secret: Option<String>,
}

impl Config {
    fn from_env() -> Result<Self> {
        let var =
            |name: &str, default: &str| std::env::var(name).unwrap_or_else(|_| default.to_owned());
        let data_dir: PathBuf = var("DATA_DIR", "data").into();
        let problems = std::env::var_os("PROBLEMS_FILE")
            .map_or_else(|| data_dir.join("problems.json"), PathBuf::from);
        Ok(Self {
            state_dir: var("STATE_DIR", "data").into(),
            data_dir,
            problems,
            site: var("SITE_ADDRESS", "http://openleet.localhost"),
            http_port: var("HTTP_PORT", "8080").parse().context("HTTP_PORT")?,
            https_port: var("HTTPS_PORT", "443").parse().context("HTTPS_PORT")?,
            judge: var("JUDGE_SOCKET", openleet_proto::DEFAULT_SOCKET).parse()?,
            deploy_secret: std::env::var("DEPLOY_SECRET").ok(),
        })
    }

    /// The HTTPS domains, primary first; `None` for plain HTTP.
    fn tls_domains(&self) -> Option<Vec<String>> {
        if self.site.starts_with("http://") {
            return None;
        }
        let domains: Vec<String> = self
            .site
            .split(',')
            .map(|d| {
                d.trim()
                    .trim_start_matches("https://")
                    .trim_end_matches('/')
            })
            .filter(|d| !d.is_empty())
            .map(str::to_owned)
            .collect();
        (!domains.is_empty()).then_some(domains)
    }
}

/// The progress database file in `state_dir`. A database from before the rename
/// (`cards.duckdb`) is moved into place once, with its write-ahead log.
fn database_path(state_dir: &Path) -> Result<PathBuf> {
    const OLD: &str = "cards.duckdb";
    const NEW: &str = "openleet.duckdb";
    let path = state_dir.join(NEW);
    let old = state_dir.join(OLD);
    if !path.exists() && old.exists() {
        std::fs::rename(&old, &path)
            .with_context(|| format!("renaming {} to {NEW}", old.display()))?;
        let old_wal = state_dir.join(format!("{OLD}.wal"));
        if old_wal.exists() {
            std::fs::rename(&old_wal, state_dir.join(format!("{NEW}.wal")))
                .context("renaming the write-ahead log")?;
        }
        tracing::info!("moved {OLD} to {NEW}");
    }
    Ok(path)
}

fn load_state(config: &Config) -> Result<Shared> {
    let content = Content::load(&config.problems, &config.data_dir.join("approaches.json"))?;
    let (store, opening) = Store::open(
        &database_path(&config.state_dir)?,
        &config.data_dir.join("judge/tests.duckdb"),
    )?;
    match &opening {
        Opening::Existing(migrated) => {
            tracing::info!("progress database at schema version {}", migrated.to);
        }
        Opening::Created => tracing::info!("created the progress database"),
        Opening::Recovered {
            quarantined,
            backup,
        } => tracing::error!(
            "progress database recovered from {}; the unusable files are in {}",
            backup.as_deref().map_or_else(
                || "nothing (it starts empty)".into(),
                |b| b.display().to_string()
            ),
            quarantined.display()
        ),
    }
    let judge = Judge::load(
        &config.data_dir.join("judge/specs.json"),
        config.judge.clone(),
    )?;
    let progress = Progress::new(
        store.attempts()?,
        store.notes()?,
        store.coding_log()?,
        store.plans()?,
    );
    let companies = api::companies_response(&content);
    Ok(Arc::new(AppState {
        companies,
        revision: deploy::revision(&config.data_dir),
        deploy: Deploy::new(config.deploy_secret.clone(), &config.state_dir),
        content,
        store,
        judge,
        progress: RwLock::new(progress),
        progress_updates: parking_lot::Mutex::new(()),
        certificate: CertificateSlot::default(),
    }))
}

fn app(state: Shared) -> Router {
    let api = api::routes().layer(
        CompressionLayer::new()
            .br(false)
            .zstd(true)
            .gzip(true)
            .quality(CompressionLevel::Fastest),
    );
    Router::new()
        .nest("/api", api)
        .fallback(assets::serve)
        .layer(axum::middleware::map_response(security::headers))
        .layer(tower::limit::GlobalConcurrencyLimitLayer::new(
            security::MAX_IN_FLIGHT,
        ))
        .with_state(state)
}

/// `openleet health`: succeeds when the server on this machine answers `GET /api/version` on
/// `HTTP_PORT` with 200 (plain HTTP mode). The container image has no shell or curl for this.
fn health() -> Result<()> {
    use std::io::{Read, Write};
    let port: u16 = std::env::var("HTTP_PORT")
        .unwrap_or_else(|_| "8080".to_owned())
        .parse()
        .context("HTTP_PORT")?;
    let address = SocketAddr::from((std::net::Ipv4Addr::LOCALHOST, port));
    let mut stream = std::net::TcpStream::connect_timeout(&address, Duration::from_secs(2))?;
    stream.set_read_timeout(Some(Duration::from_secs(5)))?;
    stream.write_all(b"GET /api/version HTTP/1.0\r\nHost: localhost\r\n\r\n")?;
    let mut status = [0; 12];
    stream.read_exact(&mut status)?;
    anyhow::ensure!(
        status.starts_with(b"HTTP/1.") && status.ends_with(b"200"),
        "unhealthy: {}",
        String::from_utf8_lossy(&status)
    );
    Ok(())
}

#[tokio::main(worker_threads = 2)]
async fn main() -> Result<()> {
    if std::env::args().nth(1).as_deref() == Some("health") {
        return health();
    }
    tracing_subscriber::fmt().with_target(false).init();
    let mut sockets = Sockets::from_systemd();
    let config = Config::from_env()?;
    let state = load_state(&config)?;
    tracing::info!(
        "OpenLeet {}: {} problems, {} attempts, {} embedded files{}",
        state.revision,
        state.content.problems.len(),
        state.progress.read().attempts.len(),
        assets::embedded(),
        if sockets.activated() {
            ", socket-activated"
        } else {
            ""
        }
    );

    let scorer = Arc::clone(&state);
    tokio::spawn(async move {
        let mut tick = tokio::time::interval(REPORT_REFRESH);
        loop {
            tick.tick().await;
            scorer.refresh_reports();
            let store = Arc::clone(&scorer);
            let _ = store.db(Store::checkpoint).await;
        }
    });

    tokio::spawn(back_up_daily(Arc::clone(&state)));
    tokio::spawn(health::watchdog(Arc::clone(&state)));

    let certificate = Arc::clone(&state.certificate);
    let router = app(state);
    let http = SocketAddr::from((Ipv6Addr::UNSPECIFIED, config.http_port));
    let stop = Shutdown::new(signal());
    match config.tls_domains() {
        None => {
            tracing::info!("serving {} on {http}", config.site);
            let listener = tokio::net::TcpListener::from_std(sockets.take("http", http)?)?;
            health::ready();
            axum::serve(listener, router)
                .with_graceful_shutdown(stop.wait())
                .await?;
        }
        Some(domains) => {
            serve_tls(
                &config,
                domains,
                router,
                &mut sockets,
                http,
                certificate,
                stop,
            )
            .await?;
        }
    }
    Ok(())
}

/// Takes the day's backup of the progress database when there is none yet (see
/// `db::backup`). The copy runs on the blocking pool and holds the database for the few
/// milliseconds a small database takes.
async fn back_up_daily(state: Shared) {
    let mut tick = tokio::time::interval(BACKUP_CHECK);
    loop {
        tick.tick().await;
        let day = jiff::Timestamp::now()
            .to_zoned(jiff::tz::TimeZone::UTC)
            .date();
        let started = std::time::Instant::now();
        match state.db(move |store| store.backup(day)).await {
            Ok(Some(backup)) => tracing::info!(
                "backup: {} ({} KiB) in {} ms",
                backup.file.display(),
                backup.bytes.div_ceil(1024),
                started.elapsed().as_millis()
            ),
            Ok(None) => {}
            Err(error) => tracing::error!("backup failed: {error}"),
        }
    }
}

/// The primary domain and the aliases that redirect to it.
#[derive(Clone)]
struct Canonical {
    primary: Arc<str>,
    aliases: Arc<[String]>,
}

impl Canonical {
    /// Where a request for `host` (with or without a port) and `path` should go instead,
    /// or `None` when the host is not an alias.
    fn redirect(&self, host: &str, path: &str) -> Option<String> {
        let name = host.rsplit_once(':').map_or(host, |(name, _)| name);
        self.aliases
            .iter()
            .any(|alias| alias.eq_ignore_ascii_case(name))
            .then(|| format!("https://{}{path}", self.primary))
    }
}

/// Permanently redirects requests for an alias domain to the same path on the primary one.
async fn canonical_host(
    State(canonical): State<Canonical>,
    request: Request,
    next: Next,
) -> Response {
    // HTTP/2 carries the host in the URI (:authority), HTTP/1.1 in the Host header.
    let host = request
        .uri()
        .authority()
        .map(Authority::as_str)
        .or_else(|| {
            request
                .headers()
                .get(header::HOST)
                .and_then(|h| h.to_str().ok())
        });
    let path = request.uri().path_and_query().map_or("/", |p| p.as_str());
    match host.and_then(|host| canonical.redirect(host, path)) {
        Some(target) => Redirect::permanent(&target).into_response(),
        None => next.run(request).await,
    }
}

/// HTTPS with one Let's Encrypt certificate for every domain (TLS-ALPN-01 on the HTTPS
/// port), the app on the first domain, the others redirecting to it, plus a plain HTTP
/// listener that only redirects.
async fn serve_tls(
    config: &Config,
    domains: Vec<String>,
    router: Router,
    sockets: &mut Sockets,
    http: SocketAddr,
    certificate: CertificateSlot,
    stop: Shutdown,
) -> Result<()> {
    let Some((primary, aliases)) = domains.split_first() else {
        anyhow::bail!("SITE_ADDRESS names no domain");
    };
    let canonical = Canonical {
        primary: primary.as_str().into(),
        aliases: aliases.into(),
    };
    let acme_state = AcmeConfig::new(domains.iter().cloned())
        .cache(ObservedCache::new(
            config.state_dir.join("acme"),
            Arc::clone(&certificate),
        ))
        .directory_lets_encrypt(true)
        .state();
    let mut rustls = (*acme_state.default_rustls_config()).clone();
    rustls.alpn_protocols = vec![b"h2".to_vec(), b"http/1.1".to_vec()];
    let acceptor = acme_state.axum_acceptor(Arc::new(rustls));
    tokio::spawn(acme::drive(acme_state, certificate));

    let host = Arc::clone(&canonical.primary);
    let redirect = Router::new().fallback(move |uri: Uri| {
        let target = format!(
            "https://{host}{}",
            uri.path_and_query().map_or("/", |p| p.as_str())
        );
        async move { Redirect::permanent(&target) }
    });
    let listener = tokio::net::TcpListener::from_std(sockets.take("http", http)?)?;
    let redirect_stop = stop.clone();
    tokio::spawn(async move {
        axum::serve(listener, redirect)
            .with_graceful_shutdown(redirect_stop.wait())
            .await
    });

    let https = SocketAddr::from((Ipv6Addr::UNSPECIFIED, config.https_port));
    let https_listener = sockets.take("https", https)?;
    tracing::info!(
        "serving https://{primary} on {https}{}",
        if aliases.is_empty() {
            String::new()
        } else {
            format!(", redirecting {}", aliases.join(", "))
        }
    );
    let handle = axum_server::Handle::new();
    let stopper = handle.clone();
    tokio::spawn(async move {
        stop.wait().await;
        stopper.graceful_shutdown(Some(DRAIN));
    });
    let mut server = axum_server::from_tcp(https_listener)?;
    // Slow clients may not hold a connection open by trickling in their headers.
    server
        .http_builder()
        .http1()
        .timer(hyper_util::rt::TokioTimer::new())
        .header_read_timeout(security::HEADER_READ_TIMEOUT);
    health::ready();
    server
        .acceptor(acceptor)
        .handle(handle)
        .serve(
            router
                .layer(axum::middleware::from_fn_with_state(
                    canonical,
                    canonical_host,
                ))
                .layer(axum::middleware::map_response(hsts))
                .into_make_service(),
        )
        .await?;
    Ok(())
}

async fn hsts(mut response: axum::response::Response) -> axum::response::Response {
    response.headers_mut().insert(
        header::STRICT_TRANSPORT_SECURITY,
        header::HeaderValue::from_static("max-age=31536000"),
    );
    response
}

/// Resolves on SIGINT or SIGTERM.
async fn signal() {
    let ctrl_c = tokio::signal::ctrl_c();
    #[cfg(unix)]
    let term = async {
        if let Ok(mut signal) =
            tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
        {
            signal.recv().await;
        }
    };
    tokio::select! {
        _ = ctrl_c => {},
        () = term => {},
    }
}

/// The server's stop, shared by its listeners: logged and reported to systemd once, however
/// many listeners wait for it.
#[derive(Clone)]
struct Shutdown(tokio::sync::watch::Receiver<bool>);

impl Shutdown {
    /// Stops when `trigger` resolves.
    fn new(trigger: impl Future<Output = ()> + Send + 'static) -> Self {
        let (stopped, receiver) = tokio::sync::watch::channel(false);
        tokio::spawn(async move {
            trigger.await;
            tracing::info!("shutting down");
            health::stopping();
            stopped.send_replace(true);
        });
        Self(receiver)
    }

    /// Resolves once the server is stopping.
    async fn wait(mut self) {
        // An error means the sender is gone, which happens only after it sent `true`.
        let _ = self.0.wait_for(|&stopped| stopped).await;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn config(site: &str) -> Config {
        Config {
            data_dir: "data".into(),
            state_dir: "data".into(),
            problems: "data/problems.json".into(),
            site: site.to_owned(),
            http_port: 8080,
            https_port: 443,
            judge: openleet_proto::DEFAULT_SOCKET
                .parse()
                .expect("default socket"),
            deploy_secret: None,
        }
    }

    #[test]
    fn reads_one_or_more_tls_domains() {
        assert_eq!(config("http://openleet.localhost").tls_domains(), None);
        assert_eq!(
            config("openleet.sudhanva.me, https://google.sudhanva.me/").tls_domains(),
            Some(vec![
                "openleet.sudhanva.me".to_owned(),
                "google.sudhanva.me".to_owned()
            ])
        );
        assert_eq!(config(" , ").tls_domains(), None);
    }

    #[test]
    fn redirects_aliases_to_the_primary_domain() {
        let canonical = Canonical {
            primary: "openleet.sudhanva.me".into(),
            aliases: vec!["google.sudhanva.me".to_owned()].into(),
        };
        assert_eq!(
            canonical.redirect("Google.sudhanva.me:443", "/problems?status=shaky"),
            Some("https://openleet.sudhanva.me/problems?status=shaky".to_owned())
        );
        assert_eq!(canonical.redirect("openleet.sudhanva.me", "/"), None);
        assert_eq!(canonical.redirect("evil.example", "/"), None);
    }

    #[test]
    fn drains_well_within_the_stop_timeout() {
        let unit = include_str!("../../deploy/openleet.service");
        let timeout = unit
            .lines()
            .find_map(|line| line.strip_prefix("TimeoutStopSec="))
            .and_then(|seconds| seconds.trim().parse::<u64>().ok())
            .expect("TimeoutStopSec in openleet.service");
        // Room left to close the database after the drain.
        assert!(DRAIN * 2 <= Duration::from_secs(timeout), "{DRAIN:?}");
    }

    #[tokio::test]
    async fn one_shutdown_reaches_every_listener() {
        let (trigger, fired) = tokio::sync::oneshot::channel::<()>();
        let stop = Shutdown::new(async {
            let _ = fired.await;
        });
        let waiters: Vec<_> = (0..3).map(|_| tokio::spawn(stop.clone().wait())).collect();
        tokio::task::yield_now().await;
        assert!(waiters.iter().all(|w| !w.is_finished()));
        trigger.send(()).unwrap();
        for waiter in waiters {
            tokio::time::timeout(Duration::from_secs(5), waiter)
                .await
                .expect("stopped")
                .unwrap();
        }
        // A listener that starts waiting after the stop returns at once.
        tokio::time::timeout(Duration::from_secs(5), stop.wait())
            .await
            .expect("already stopped");
    }

    #[test]
    fn moves_the_old_database_once() {
        let dir = std::env::temp_dir().join(format!("openleet-main-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).expect("temp dir");
        std::fs::write(dir.join("cards.duckdb"), b"db").expect("write");
        std::fs::write(dir.join("cards.duckdb.wal"), b"wal").expect("write");
        let path = database_path(&dir).expect("move");
        assert_eq!(path, dir.join("openleet.duckdb"));
        assert_eq!(std::fs::read(&path).expect("moved"), b"db");
        assert!(dir.join("openleet.duckdb.wal").exists() && !dir.join("cards.duckdb").exists());
        // A new database is never replaced by an old one.
        std::fs::write(dir.join("cards.duckdb"), b"older").expect("write");
        database_path(&dir).expect("keep");
        assert_eq!(std::fs::read(&path).expect("kept"), b"db");
        let _ = std::fs::remove_dir_all(&dir);
    }
}
