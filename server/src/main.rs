//! The flashcard and coding server: JSON API, embedded web app, and automatic HTTPS.

mod api;
mod assets;
mod db;
mod error;
mod judge;
mod state;

use std::collections::HashSet;
use std::net::{Ipv6Addr, SocketAddr};
use std::path::PathBuf;
use std::sync::Arc;
use std::time::Duration;

use anyhow::{Context, Result};
use axum::Router;
use axum::http::{Uri, header};
use axum::response::Redirect;
use parking_lot::RwLock;
use rustls_acme::AcmeConfig;
use rustls_acme::caches::DirCache;
use tokio_stream::StreamExt;
use tower_http::CompressionLevel;
use tower_http::compression::CompressionLayer;

use cards::content::Content;

use crate::db::Store;
use crate::judge::Judge;
use crate::state::{AppState, Progress, Shared};

#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

/// How often today's scores are saved even without new attempts (memory decays over time).
const SCORE_REFRESH: Duration = Duration::from_secs(15 * 60);

struct Config {
    data_dir: PathBuf,
    state_dir: PathBuf,
    /// `http://host` serves plain HTTP; a bare domain gets an HTTPS certificate.
    site: String,
    http_port: u16,
    https_port: u16,
    judge: judge_proto::Endpoint,
    cpu_scale: f64,
}

impl Config {
    fn from_env() -> Result<Self> {
        let var =
            |name: &str, default: &str| std::env::var(name).unwrap_or_else(|_| default.to_owned());
        Ok(Self {
            data_dir: var("DATA_DIR", "data").into(),
            state_dir: var("STATE_DIR", "data").into(),
            site: var("SITE_ADDRESS", "http://google.localhost"),
            http_port: var("HTTP_PORT", "8080").parse().context("HTTP_PORT")?,
            https_port: var("HTTPS_PORT", "443").parse().context("HTTPS_PORT")?,
            judge: var("JUDGE_SOCKET", judge_proto::DEFAULT_SOCKET).parse()?,
            cpu_scale: var("JUDGE_CPU_SCALE", "2.5")
                .parse()
                .context("JUDGE_CPU_SCALE")?,
        })
    }

    fn tls_domain(&self) -> Option<&str> {
        (!self.site.starts_with("http://")).then(|| self.site.trim_start_matches("https://"))
    }
}

fn load_state(config: &Config) -> Result<Shared> {
    let content = Content::load(&config.data_dir)?;
    let store = Store::open(
        &config.state_dir.join("cards.duckdb"),
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
    let progress = Progress::new(
        store.attempts()?,
        store.notes()?,
        store.solved()?.into_iter().collect::<HashSet<_>>(),
    );
    Ok(Arc::new(AppState {
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
    let config = Config::from_env()?;
    let state = load_state(&config)?;
    tracing::info!(
        "{} problems, {} attempts, {} embedded files",
        state.content.problems.len(),
        state.progress.read().attempts.len(),
        assets::embedded()
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
            let _ = store.db(|s| s.checkpoint()).await;
        }
    });

    let router = app(state);
    let http = SocketAddr::from((Ipv6Addr::UNSPECIFIED, config.http_port));
    match config.tls_domain() {
        None => {
            tracing::info!("serving {} on {http}", config.site);
            let listener = tokio::net::TcpListener::bind(http).await?;
            axum::serve(listener, router)
                .with_graceful_shutdown(shutdown())
                .await?;
        }
        Some(domain) => serve_tls(&config, domain, router, http).await?,
    }
    Ok(())
}

/// HTTPS with a Let's Encrypt certificate (TLS-ALPN-01 on the HTTPS port), plus a plain
/// HTTP listener that only redirects.
async fn serve_tls(config: &Config, domain: &str, router: Router, http: SocketAddr) -> Result<()> {
    let mut acme = AcmeConfig::new([domain.to_owned()])
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

    let host = domain.to_owned();
    let redirect = Router::new().fallback(move |uri: Uri| {
        let target = format!(
            "https://{host}{}",
            uri.path_and_query().map_or("/", |p| p.as_str())
        );
        async move { Redirect::permanent(&target) }
    });
    let listener = tokio::net::TcpListener::bind(http).await?;
    tokio::spawn(async move { axum::serve(listener, redirect).await });

    let https = SocketAddr::from((Ipv6Addr::UNSPECIFIED, config.https_port));
    tracing::info!("serving https://{domain} on {https}");
    let handle = axum_server::Handle::new();
    let stopper = handle.clone();
    tokio::spawn(async move {
        shutdown().await;
        stopper.graceful_shutdown(Some(Duration::from_secs(5)));
    });
    axum_server::bind(https)
        .acceptor(acceptor)
        .handle(handle)
        .serve(
            router
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
