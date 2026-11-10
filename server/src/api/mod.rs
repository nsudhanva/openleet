//! The JSON API under /api (shapes documented in web/src/lib/types.ts).
//!
//! Responses that hold `f32` frequencies are serialized straight to text with `Json(&value)`,
//! never through `json!` / `serde_json::Value`, which would widen 93.2 to 93.19999694824219.

mod code;
mod plans;
mod study;

use std::collections::HashMap;

use axum::extract::{DefaultBodyLimit, Query, State};
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
pub fn routes() -> Router<Shared> {
    let judged = Router::new()
        .route("/run", post(code::run))
        .route("/submit", post(code::submit))
        .layer(security::timeout(security::JUDGE_TIMEOUT));
    Router::new()
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
