//! The JSON API under /api (shapes documented in web/src/lib/types.ts).

use std::collections::HashMap;

use axum::extract::{Path, Query, State};
use axum::http::StatusCode;
use axum::response::IntoResponse;
use axum::routing::{get, post, put};
use axum::{Json, Router};
use serde::Deserialize;
use serde_json::json;

use cards::service::{self, AttemptInput, DeckQuery};

use crate::db::NewSubmission;
use crate::error::{ApiError, ApiResult};
use crate::judge::{self, Shown, show_input, show_value};
use crate::state::{Shared, now_ms};

const MAX_NOTE_CHARS: usize = 4000;
const SEARCH_LIMIT: usize = 20;
const MAX_SEARCH_LIMIT: usize = 2000;
const HISTORY_DAYS: usize = 60;
const SUBMISSIONS_SHOWN: usize = 50;

pub fn routes() -> Router<Shared> {
    Router::new()
        .route("/deck", get(deck))
        .route("/attempts", post(record_attempt))
        .route("/notes", put(save_note))
        .route("/progress", axum::routing::delete(reset_progress))
        .route("/problems", get(problems))
        .route("/problems/{slug}", get(problem))
        .route("/search", get(search))
        .route("/report", get(report))
        .route("/readiness", get(readiness))
        .route("/code/{slug}", get(code_info))
        .route("/drafts", put(save_draft))
        .route("/run", post(run))
        .route("/submit", post(submit))
        .route("/submissions", get(submissions))
        .route("/submissions/{id}", get(submission))
        .fallback(|| async { ApiError::NotFound("No such endpoint".into()) })
}

type Params = Query<HashMap<String, String>>;

fn param<'a>(params: &'a HashMap<String, String>, key: &str) -> Option<&'a str> {
    params.get(key).map(String::as_str)
}

// ---- Study ------------------------------------------------------------------------------------

async fn deck(State(state): State<Shared>, Query(params): Params) -> impl IntoResponse {
    let query = DeckQuery::from_params(
        param(&params, "set"),
        param(&params, "period"),
        param(&params, "topic"),
        param(&params, "difficulty"),
        param(&params, "slug"),
    );
    let progress = state.progress.read();
    let deck = service::deck(&state.content, &progress.states, &query, now_ms(), |slug| {
        progress.notes.get(slug).cloned()
    });
    Json(json!(deck))
}

async fn record_attempt(
    State(state): State<Shared>,
    Json(input): Json<AttemptInput>,
) -> ApiResult<impl IntoResponse> {
    input.validate()?;
    let attempt = service::new_attempt(&state.content, input, now_ms())?;
    let score = attempt.score;
    let stored = attempt.clone();
    state.db(move |store| store.insert_attempt(&stored)).await?;
    state.progress.write().push(attempt);
    state.refresh_scores().await?;
    Ok((StatusCode::CREATED, Json(json!({ "score": score }))))
}

#[derive(Deserialize)]
struct NoteInput {
    slug: String,
    text: String,
}

async fn save_note(
    State(state): State<Shared>,
    Json(input): Json<NoteInput>,
) -> ApiResult<impl IntoResponse> {
    service::problem_of(&state.content, &input.slug)?;
    let text = input.text.trim().to_owned();
    if text.chars().count() > MAX_NOTE_CHARS {
        return Err(ApiError::BadRequest(format!(
            "Notes are at most {MAX_NOTE_CHARS} characters"
        )));
    }
    let (slug, stored) = (input.slug.clone(), text.clone());
    state
        .db(move |store| store.save_note(&slug, &stored, now_ms()))
        .await?;
    let mut progress = state.progress.write();
    if text.is_empty() {
        progress.notes.remove(&input.slug);
    } else {
        progress.notes.insert(input.slug, text.clone());
    }
    Ok(Json(json!({ "note": (!text.is_empty()).then_some(text) })))
}

/// `?slug=two-sum` clears one problem, `?all=true` everything; anything else is rejected.
async fn reset_progress(
    State(state): State<Shared>,
    Query(params): Params,
) -> ApiResult<StatusCode> {
    let slug = match (param(&params, "slug"), param(&params, "all"), params.len()) {
        (Some(slug), None, 1) if !slug.is_empty() => {
            Some(service::problem_of(&state.content, slug)?.slug.clone())
        }
        (None, Some("true"), 1) => None,
        _ => return Err(ApiError::BadRequest("Give either slug or all=true".into())),
    };
    let target = slug.clone();
    state
        .db(move |store| store.delete_attempts(target.as_deref()))
        .await?;
    state.progress.write().clear(slug.as_deref());
    Ok(StatusCode::NO_CONTENT)
}

async fn problems(State(state): State<Shared>) -> impl IntoResponse {
    let progress = state.progress.read();
    Json(json!(service::problem_rows(
        &state.content,
        &progress.states,
        now_ms()
    )))
}

async fn problem(
    State(state): State<Shared>,
    Path(slug): Path<String>,
) -> ApiResult<impl IntoResponse> {
    let progress = state.progress.read();
    let note = progress.notes.get(&slug).cloned();
    Ok(Json(json!(service::card(
        &state.content,
        &progress.states,
        &slug,
        note
    )?)))
}

async fn search(
    State(state): State<Shared>,
    Query(params): Params,
) -> ApiResult<impl IntoResponse> {
    let q = param(&params, "q").unwrap_or_default();
    let limit = match param(&params, "limit") {
        Some(text) => text
            .parse::<usize>()
            .map_err(|_| ApiError::BadRequest("limit must be a number".into()))?,
        None => SEARCH_LIMIT,
    };
    Ok(Json(json!(
        state.content.search(q, limit.clamp(1, MAX_SEARCH_LIMIT))
    )))
}

async fn report(State(state): State<Shared>) -> ApiResult<impl IntoResponse> {
    let history = state.db(|store| store.daily_scores(HISTORY_DAYS)).await?;
    let mut progress = state.progress.write();
    let report = progress.report(&state.content, now_ms(), false);
    Ok(Json(json!({ "report": report, "history": history })))
}

async fn readiness(State(state): State<Shared>) -> impl IntoResponse {
    let mut progress = state.progress.write();
    Json(json!({ "readiness": progress.report(&state.content, now_ms(), false).readiness }))
}

// ---- Code -------------------------------------------------------------------------------------

async fn code_info(
    State(state): State<Shared>,
    Path(slug): Path<String>,
) -> ApiResult<impl IntoResponse> {
    service::problem_of(&state.content, &slug)?;
    let entry = state.judge.entry(&slug);
    let (lookup, draft_slug) = (slug.clone(), slug.clone());
    let tests = state.db(move |store| store.tests(&lookup)).await?;
    let draft = state.db(move |store| store.draft(&draft_slug)).await?;
    let examples: Vec<Shown> = match entry {
        Some(entry) => tests
            .iter()
            .filter(|t| t.kind == "example")
            .map(|t| Shown {
                input: show_input(entry, &t.test),
                expected: show_value(&t.expected),
            })
            .collect(),
        None => Vec::new(),
    };
    let supported = entry.is_some_and(|e| e.supported) && !tests.is_empty();
    let reason = match entry {
        Some(e) if !e.supported => e.reason.clone(),
        None => Some("This problem cannot be judged yet.".into()),
        _ if tests.is_empty() => Some("This problem has no tests yet.".into()),
        _ => None,
    };
    let solved = state.progress.read().solved.contains(&slug);
    Ok(Json(json!({
        "slug": slug,
        "starter": entry.and_then(|e| e.starter.clone()),
        "draft": draft,
        "judge": {
            "supported": supported,
            "reason": reason,
            "examples": entry.map_or(0, |e| e.tests.example),
            "hidden": entry.map_or(0, |e| e.tests.hidden),
            "stress": entry.map_or(0, |e| e.tests.stress),
            "timeLimitMs": entry.filter(|_| supported).map(|e| state.judge.time.limit_ms(e)),
        },
        "examples": examples,
        "solved": solved,
    })))
}

#[derive(Deserialize)]
struct DraftInput {
    slug: String,
    code: String,
}

async fn save_draft(
    State(state): State<Shared>,
    Json(input): Json<DraftInput>,
) -> ApiResult<StatusCode> {
    service::problem_of(&state.content, &input.slug)?;
    state
        .db(move |store| store.save_draft(&input.slug, &input.code, now_ms()))
        .await?;
    Ok(StatusCode::NO_CONTENT)
}

#[derive(Deserialize)]
struct RunInput {
    slug: String,
    code: String,
    input: Option<String>,
}

fn judged<'a>(state: &'a Shared, slug: &str) -> ApiResult<&'a judge::Entry> {
    service::problem_of(&state.content, slug)?;
    state
        .judge
        .entry(slug)
        .filter(|e| e.supported)
        .ok_or_else(|| ApiError::BadRequest("This problem cannot be judged yet".into()))
}

async fn run(
    State(state): State<Shared>,
    Json(input): Json<RunInput>,
) -> ApiResult<impl IntoResponse> {
    let entry = judged(&state, &input.slug)?;
    let slug = input.slug.clone();
    let mut tests = state.db(move |store| store.tests(&slug)).await?;
    tests.retain(|t| t.kind == "example");
    let custom = input
        .input
        .as_deref()
        .filter(|text| !text.trim().is_empty());
    Ok(Json(
        state.judge.run(entry, &tests, &input.code, custom).await?,
    ))
}

#[derive(Deserialize)]
struct SubmitInput {
    slug: String,
    code: String,
}

async fn submit(
    State(state): State<Shared>,
    Json(input): Json<SubmitInput>,
) -> ApiResult<impl IntoResponse> {
    let entry = judged(&state, &input.slug)?;
    let slug = input.slug.clone();
    let tests = state.db(move |store| store.tests(&slug)).await?;
    let (outcome, limit_ms) = state.judge.submit(entry, &tests, &input.code).await?;
    let mut result = judge::submit_result(entry, &tests, &outcome, limit_ms, 0);
    let detail = json!({ "failing": result.failing, "error": result.error, "limitMs": limit_ms })
        .to_string();
    // A fault of the judge is not the solution's: report it without recording it.
    if outcome.verdict == judge_proto::Verdict::InternalError {
        return Ok(Json(result));
    }
    let (slug, code, verdict) = (input.slug.clone(), input.code, result.verdict);
    let (passed, total, cpu_ms) = (result.passed, result.total, result.cpu_ms);
    result.id = state
        .db(move |store| {
            store.insert_submission(&NewSubmission {
                slug: &slug,
                at: now_ms(),
                code: &code,
                verdict,
                passed,
                total,
                cpu_ms,
                detail: &detail,
            })
        })
        .await?;
    if result.verdict == "accepted" {
        state.progress.write().solved.insert(input.slug);
    }
    Ok(Json(result))
}

async fn submissions(
    State(state): State<Shared>,
    Query(params): Params,
) -> ApiResult<impl IntoResponse> {
    let slug = param(&params, "slug")
        .ok_or_else(|| ApiError::BadRequest("slug is required".into()))?
        .to_owned();
    service::problem_of(&state.content, &slug)?;
    Ok(Json(
        state
            .db(move |store| store.submissions(&slug, SUBMISSIONS_SHOWN))
            .await?,
    ))
}

async fn submission(
    State(state): State<Shared>,
    Path(id): Path<i64>,
) -> ApiResult<impl IntoResponse> {
    state
        .db(move |store| store.submission(id))
        .await?
        .map(Json)
        .ok_or_else(|| ApiError::NotFound(format!("No submission {id}")))
}
