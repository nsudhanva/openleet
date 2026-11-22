//! The JSON API under /api (shapes documented in web/src/lib/types.ts).
//!
//! Responses that hold `f32` frequencies are serialized straight to text with `Json(&value)`,
//! never through `json!` / `serde_json::Value`, which would widen 93.2 to 93.19999694824219.

mod account;
mod code;
mod lists;
mod plans;
mod study;

use std::collections::HashMap;

use axum::extract::{DefaultBodyLimit, Query, State};
use axum::http::{HeaderValue, header};
use axum::response::{IntoResponse, Response};
use axum::routing::{delete, get, patch, post, put};
use axum::{Json, Router};
use serde::Serialize;

use crate::error::ApiError;
use crate::state::Shared;
use crate::{deploy, security};

pub use study::companies_response;

/// Every endpoint, relative to /api. Run and Submit may take up to
/// [`security::JUDGE_TIMEOUT`]; everything else [`security::REQUEST_TIMEOUT`].
///
/// Content endpoints (companies, topics, search) and the server's own (session, version,
/// health, deploy) are public. Every other endpoint takes [`crate::auth::Me`]: it answers
/// 401 without a session and reads and writes only the signed-in account's progress. Its
/// answers are private to the account (`Cache-Control: private`, `Vary: Cookie`).
pub fn routes() -> Router<Shared> {
    let judged = Router::new()
        .route("/run", post(code::run))
        .route("/submit", post(code::submit))
        .layer(security::timeout(security::JUDGE_TIMEOUT));
    Router::new()
        .route(
            "/session",
            get(account::session)
                .post(account::sign_in)
                .delete(account::sign_out),
        )
        .route("/users", post(account::sign_up))
        .route("/account", delete(account::delete_account))
        .route("/account/password", put(account::change_password))
        .route(
            "/admin/settings",
            get(account::settings).patch(account::edit_settings),
        )
        .route("/companies", get(study::companies))
        .route("/topics", get(study::topics))
        .route("/deck", get(study::deck))
        .route("/attempts", post(study::record_attempt))
        .route("/notes", put(study::save_note))
        .route("/progress", delete(study::reset_progress))
        .route("/problems", get(study::problems))
        .route("/problems/{slug}", get(study::problem))
        .route("/search", get(study::search))
        .route("/report", get(study::report))
        .route("/readiness", get(study::readiness))
        .route("/next", get(plans::next))
        .route("/plans", get(plans::plans).put(plans::use_plan))
        .route(
            "/plans/{id}",
            patch(plans::edit_plan).delete(plans::delete_plan),
        )
        .route("/lists", get(lists::lists).post(lists::create_list))
        .route(
            "/lists/{id}",
            patch(lists::edit_list).delete(lists::delete_list),
        )
        .route("/code/{slug}", get(code::code_info))
        .route("/drafts", put(code::save_draft))
        .route("/drafts/reset", post(code::reset_draft))
        .route("/drafts/restore", post(code::restore_draft))
        .route("/submissions", get(code::submissions))
        .route("/submissions/{id}", get(code::submission))
        .route("/version", get(version))
        .route("/health", get(crate::health::health))
        .route(
            "/deploy",
            post(deploy::deploy).layer(DefaultBodyLimit::max(deploy::MAX_BODY)),
        )
        .layer(security::timeout(security::REQUEST_TIMEOUT))
        .merge(judged)
        .fallback(|| async { ApiError::no_endpoint() })
        .layer(axum::middleware::map_response(crate::error::json_errors))
        .layer(axum::middleware::map_response(private))
}

/// Keeps answers out of shared caches: most are one account's. Answers that set their own
/// `Cache-Control` (the public, revalidated content) keep it.
async fn private(mut response: Response) -> Response {
    let headers = response.headers_mut();
    if !headers.contains_key(header::CACHE_CONTROL) {
        headers.insert(header::CACHE_CONTROL, HeaderValue::from_static("private"));
    }
    headers.insert(header::VARY, HeaderValue::from_static("cookie"));
    response
}

/// A request's query string.
type Params = Query<HashMap<String, String>>;

fn param<'a>(params: &'a HashMap<String, String>, key: &str) -> Option<&'a str> {
    params.get(key).map(String::as_str)
}

#[derive(Serialize)]
struct Version<'a> {
    revision: &'a str,
}

/// The running release, so CI can wait for a deploy to go live.
async fn version(State(state): State<Shared>) -> Response {
    Json(&Version {
        revision: &state.revision,
    })
    .into_response()
}

/// The handler tests' fixtures.
#[cfg(test)]
pub mod testing {
    use std::path::Path;

    use axum::extract::Query;
    use axum::response::Response;
    use openleet::content::Content;

    use super::Params;
    use crate::db::testing::TempDir;
    use crate::state::{Shared, test_state_with};

    /// A state over the real problems, a new database in `dir` and no judge.
    pub fn state(dir: &TempDir) -> Shared {
        let data = Path::new(env!("CARGO_MANIFEST_DIR")).join("../data");
        let content = Content::load(
            &data.join("problems.json"),
            &data.join("approaches.json"),
            &data.join("videos.json"),
        )
        .expect("load the problems file");
        test_state_with(dir.root(), "tcp://127.0.0.1:1", content)
    }

    /// The tests' account, made on first use.
    pub async fn me(state: &Shared) -> crate::auth::Me {
        as_user(state, "learner@example.com").await
    }

    /// The account with `email`, made on first use, signed in.
    pub async fn as_user(state: &Shared, email: &str) -> crate::auth::Me {
        const HASH: &str = "$argon2id$v=19$m=19456,t=2,p=1$c2FsdA$aGFzaA";
        let user = match state.store.credentials(email).expect("look up") {
            Some(found) => found.user.id,
            None => match state
                .store
                .create_user(email, HASH, false, 1)
                .expect("create")
            {
                crate::db::NewUser::Created(id) => id,
                other => panic!("{other:?}"),
            },
        };
        crate::auth::Me::test(state, user).await
    }

    pub fn query(pairs: &[(&str, &str)]) -> Params {
        Query(
            pairs
                .iter()
                .map(|&(k, v)| (k.to_owned(), v.to_owned()))
                .collect(),
        )
    }

    pub async fn json(response: Response) -> serde_json::Value {
        let body = axum::body::to_bytes(response.into_body(), 1 << 24)
            .await
            .expect("body");
        serde_json::from_slice(&body).expect("json")
    }
}
