//! Liveness: `GET /api/health`, and systemd's readiness and watchdog notifications
//! (`Type=notify`, `WatchdogSec=` in deploy/openleet.service). Without `NOTIFY_SOCKET` (local
//! runs) the notifications do nothing.

use std::time::Duration;

use axum::Json;
use axum::extract::State;
use axum::http::{StatusCode, header};
use axum::response::{IntoResponse, Response};
use sd_notify::NotifyState;
use serde::Serialize;

use crate::acme::Certificate;
use crate::state::Shared;

/// How long a health check waits for the database connection (another query may hold it).
const DB_WAIT: Duration = Duration::from_secs(2);
/// How long a health check may take in all before the database counts as down.
const DB_TIMEOUT: Duration = Duration::from_secs(5);

#[derive(Serialize)]
struct Health<'a> {
    ok: bool,
    revision: &'a str,
    db: &'static str,
    judge: &'static str,
    certificate: Option<Certificate>,
}

const fn status(up: bool) -> &'static str {
    if up { "ok" } else { "down" }
}

/// `{"ok", "revision", "db", "judge", "certificate": {"domains", "expires_at"} | null}`:
/// 200 while the database answers, else 503 with the same body. The judge is probed by
/// connecting (cached for a few seconds), never by sending it a job.
pub async fn health(State(state): State<Shared>) -> Response {
    let (db, judge) = tokio::join!(database_answers(&state), state.judge.reachable());
    let certificate = state.certificate.read().clone();
    let body = Health {
        ok: db,
        revision: &state.revision,
        db: status(db),
        judge: status(judge),
        certificate,
    };
    let code = if db {
        StatusCode::OK
    } else {
        StatusCode::SERVICE_UNAVAILABLE
    };
    (code, [(header::CACHE_CONTROL, "no-store")], Json(&body)).into_response()
}

/// Whether the database answers a trivial query in time, through the blocking pool (so a
/// starved pool counts as down too).
async fn database_answers(state: &Shared) -> bool {
    let ping = state.db(|store| Ok(store.ping(DB_WAIT)));
    matches!(tokio::time::timeout(DB_TIMEOUT, ping).await, Ok(Ok(true)))
}

fn notify(what: &NotifyState<'_>) {
    if let Err(error) = sd_notify::notify(std::slice::from_ref(what)) {
        tracing::warn!("systemd notify {what}: {error}");
    }
}

/// Tells systemd the server is up (after migrations, imports and binding the listeners).
pub fn ready() {
    notify(&NotifyState::Ready);
}

/// Tells systemd the server is stopping.
pub fn stopping() {
    notify(&NotifyState::Stopping);
}

/// Pets systemd's watchdog every half period while the server is healthy: this task getting
/// to run on time shows the async runtime is responsive, and the database must answer a
/// trivial query. When either fails the pings stop, and systemd restarts the server once
/// `WatchdogSec` passes without one.
pub async fn watchdog(state: Shared) {
    let Some(period) = sd_notify::watchdog_enabled() else {
        return;
    };
    let every = period / 2;
    tracing::info!(
        "systemd watchdog: {} s, pinging every {} s",
        period.as_secs(),
        every.as_secs()
    );
    let mut tick = tokio::time::interval(every);
    tick.set_missed_tick_behavior(tokio::time::MissedTickBehavior::Delay);
    loop {
        let due = tick.tick().await;
        let late = due.elapsed();
        if late > every / 2 {
            tracing::warn!(
                "watchdog: the runtime ran this check {} ms late",
                late.as_millis()
            );
        }
        if database_answers(&state).await {
            notify(&NotifyState::Watchdog);
        } else {
            tracing::error!(
                "watchdog: the database did not answer within {} s; not pinging systemd",
                DB_TIMEOUT.as_secs()
            );
        }
    }
}

#[cfg(test)]
mod tests {
    use std::sync::Arc;

    use super::*;

    #[test]
    fn health_has_the_documented_shape() {
        let body = Health {
            ok: true,
            revision: "abc123",
            db: status(true),
            judge: status(false),
            certificate: Some(Certificate {
                domains: vec!["openleet.sudhanva.me".into()],
                expires_at: 1_800_000_000_000,
                issued_at: 1_792_224_000_000,
            }),
        };
        assert_eq!(
            serde_json::to_value(&body).unwrap(),
            serde_json::json!({
                "ok": true,
                "revision": "abc123",
                "db": "ok",
                "judge": "down",
                "certificate": {"domains": ["openleet.sudhanva.me"], "expires_at": 1_800_000_000_000_i64},
            })
        );
        let plain = Health {
            certificate: None,
            ..body
        };
        assert_eq!(
            serde_json::to_value(&plain).unwrap()["certificate"],
            serde_json::Value::Null
        );
    }

    async fn get(state: Shared) -> (StatusCode, serde_json::Value) {
        let response = health(State(state)).await;
        let status = response.status();
        let body = axum::body::to_bytes(response.into_body(), 1 << 16)
            .await
            .unwrap();
        (status, serde_json::from_slice(&body).unwrap())
    }

    #[tokio::test]
    #[allow(
        clippy::await_holding_lock,
        reason = "holding the database while the check runs is the point"
    )]
    async fn reports_the_database_and_the_judge() {
        let dir = crate::db::testing::TempDir::new("health");
        // Nothing listens on port 1: the judge is down.
        let (status, body) = get(crate::state::test_state(dir.root(), "tcp://127.0.0.1:1")).await;
        assert_eq!(status, StatusCode::OK);
        assert_eq!(
            (
                &body["ok"],
                &body["db"],
                &body["judge"],
                &body["certificate"]
            ),
            (
                &true.into(),
                &"ok".into(),
                &"down".into(),
                &serde_json::Value::Null
            )
        );

        let judge = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let address = format!("tcp://{}", judge.local_addr().unwrap());
        let dir = crate::db::testing::TempDir::new("health-up");
        let state = crate::state::test_state(dir.root(), &address);
        *state.certificate.write() = Some(Certificate {
            domains: vec!["a.example".into()],
            expires_at: 2,
            issued_at: 1,
        });
        let (_, body) = get(Arc::clone(&state)).await;
        assert_eq!(body["judge"], "ok");
        assert_eq!(body["certificate"]["expires_at"], 2);

        // A database that does not answer in time makes the server unhealthy.
        let held = state.store.hold();
        let (status, body) = get(Arc::clone(&state)).await;
        drop(held);
        assert_eq!(status, StatusCode::SERVICE_UNAVAILABLE);
        assert_eq!((&body["ok"], &body["db"]), (&false.into(), &"down".into()));
    }
}
