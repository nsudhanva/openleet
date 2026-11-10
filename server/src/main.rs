//! The OpenLeet server: flashcards and coding practice. JSON API, embedded web app, and
//! automatic HTTPS.

mod api;
mod assets;
mod db;
mod deploy;
mod error;
mod fingerprint;
mod judge;
mod listen;
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
use rustls_acme::caches::DirCache;
use tokio_stream::StreamExt;
use tower_http::CompressionLevel;
use tower_http::compression::CompressionLayer;

use openleet::content::Content;

use crate::db::Store;
use crate::deploy::Deploy;
use crate::judge::Judge;
use crate::listen::Sockets;
use crate::state::{AppState, Progress, Shared};

#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

/// How often today's scores are saved even without new attempts (memory decays over time).
const SCORE_REFRESH: Duration = Duration::from_mins(15);
/// How long a stopping server waits for in-flight HTTPS requests (a submission can take
/// several seconds to judge).
const DRAIN: Duration = Duration::from_secs(30);

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
    cpu_scale: f64,
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
            cpu_scale: var("JUDGE_CPU_SCALE", "2.5")
                .parse()
                .context("JUDGE_CPU_SCALE")?,
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
    let store = Store::open(
        &database_path(&config.state_dir)?,
        &config.data_dir.join("judge/tests.duckdb"),
    )?;
    let imported = store.import_sqlite(&config.state_dir.join("progress.db"))?;
    if imported > 0 {
        tracing::info!("imported {imported} attempts from the old SQLite database");
    }
    let judge = Judge::load(
        &config.data_dir.join("judge/specs.json"),
        config.judge.clone(),
        config.cpu_scale,
    )?;
    let progress = Progress::new(store.attempts()?, store.notes()?, store.solved()?);
    let companies = api::companies_response(&content);
    Ok(Arc::new(AppState {
        companies,
        revision: deploy::revision(&config.data_dir),
        deploy: Deploy::new(config.deploy_secret.clone(), &config.state_dir),
        content,
        store,
        judge,
        progress: RwLock::new(progress),
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
        .with_state(state)
}

#[tokio::main(worker_threads = 2)]
async fn main() -> Result<()> {
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
        let mut tick = tokio::time::interval(SCORE_REFRESH);
        loop {
            tick.tick().await;
            if let Err(error) = scorer.refresh_scores().await {
                tracing::warn!("scorer: {error}");
            }
            let store = Arc::clone(&scorer);
            let _ = store.db(Store::checkpoint).await;
        }
    });

    let router = app(state);
    let http = SocketAddr::from((Ipv6Addr::UNSPECIFIED, config.http_port));
    match config.tls_domains() {
        None => {
            tracing::info!("serving {} on {http}", config.site);
            let listener = tokio::net::TcpListener::from_std(sockets.take("http", http)?)?;
            axum::serve(listener, router)
                .with_graceful_shutdown(shutdown())
                .await?;
        }
        Some(domains) => serve_tls(&config, domains, router, &mut sockets, http).await?,
    }
    Ok(())
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
) -> Result<()> {
    let Some((primary, aliases)) = domains.split_first() else {
        anyhow::bail!("SITE_ADDRESS names no domain");
    };
    let canonical = Canonical {
        primary: primary.as_str().into(),
        aliases: aliases.into(),
    };
    let mut acme = AcmeConfig::new(domains.iter().cloned())
        .cache(DirCache::new(config.state_dir.join("acme")))
        .directory_lets_encrypt(true)
        .state();
    let mut rustls = (*acme.default_rustls_config()).clone();
    rustls.alpn_protocols = vec![b"h2".to_vec(), b"http/1.1".to_vec()];
    let acceptor = acme.axum_acceptor(Arc::new(rustls));
    tokio::spawn(async move {
        while let Some(event) = acme.next().await {
            match event {
                Ok(ok) => tracing::info!("acme: {ok:?}"),
                Err(error) => tracing::error!("acme: {error:?}"),
            }
        }
    });

    let host = Arc::clone(&canonical.primary);
    let redirect = Router::new().fallback(move |uri: Uri| {
        let target = format!(
            "https://{host}{}",
            uri.path_and_query().map_or("/", |p| p.as_str())
        );
        async move { Redirect::permanent(&target) }
    });
    let listener = tokio::net::TcpListener::from_std(sockets.take("http", http)?)?;
    tokio::spawn(async move {
        axum::serve(listener, redirect)
            .with_graceful_shutdown(shutdown())
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
        shutdown().await;
        stopper.graceful_shutdown(Some(DRAIN));
    });
    axum_server::from_tcp(https_listener)?
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

async fn shutdown() {
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
    tracing::info!("shutting down");
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
            cpu_scale: 1.0,
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
            canonical.redirect("Google.sudhanva.me:443", "/study?set=due"),
            Some("https://openleet.sudhanva.me/study?set=due".to_owned())
        );
        assert_eq!(canonical.redirect("openleet.sudhanva.me", "/"), None);
        assert_eq!(canonical.redirect("evil.example", "/"), None);
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
