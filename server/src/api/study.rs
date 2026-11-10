//! Flashcard endpoints: companies, deck, attempts, notes, progress, problems, search, report.

use axum::Json;
use axum::body::Bytes;
use axum::extract::{Path, Query, State};
use axum::http::{HeaderMap, HeaderValue, StatusCode, header};
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use openleet::content::Content;
use openleet::scorer::ScoreReport;
use openleet::service::{self, AttemptInput, DeckParams, DeckQuery};

use super::{Params, param};
use crate::db::DailyScore;
use crate::error::{ApiError, ApiResult};
use crate::fingerprint;
use crate::state::{Shared, now_ms};

const MAX_NOTE_CHARS: usize = 4000;
const SEARCH_LIMIT: usize = 20;
const MAX_SEARCH_LIMIT: usize = 2000;
const HISTORY_DAYS: usize = 60;

/// `GET /api/companies` as sent, with its `ETag`; built once at start-up.
pub fn companies_response(content: &Content) -> (Bytes, HeaderValue) {
    let body = content.companies_json().as_bytes();
    let etag = HeaderValue::from_str(&fingerprint::etag(body))
        .unwrap_or_else(|_| HeaderValue::from_static("\"companies\""));
    (Bytes::copy_from_slice(body), etag)
}

/// Companies change only with the data, so clients revalidate with the `ETag`.
pub async fn companies(State(state): State<Shared>, headers: HeaderMap) -> Response {
    let (body, etag) = &state.companies;
    let head = [
        (
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/json"),
        ),
        (header::CACHE_CONTROL, HeaderValue::from_static("no-cache")),
        (header::ETAG, etag.clone()),
    ];
    if headers.get(header::IF_NONE_MATCH) == Some(etag) {
        (StatusCode::NOT_MODIFIED, head).into_response()
    } else {
        (head, body.clone()).into_response()
    }
}

/// `?set=&company=&period=&topic=&difficulty=&slug=`: the next card and the cards left.
pub async fn deck(State(state): State<Shared>, Query(params): Params) -> Response {
    let query = DeckQuery::parse(
        &state.content,
        &DeckParams {
            set: param(&params, "set"),
            company: param(&params, "company"),
            period: param(&params, "period"),
            topic: param(&params, "topic"),
            difficulty: param(&params, "difficulty"),
            slug: param(&params, "slug"),
        },
    );
    let progress = state.progress.read();
    let deck = service::deck(&state.content, &progress.states, &query, now_ms(), |slug| {
        progress.notes.get(slug).cloned()
    });
    Json(&deck).into_response()
}

#[derive(Serialize)]
struct Scored {
    score: Option<f64>,
}

/// Records a graded (or skipped) answer and returns its topic score.
pub async fn record_attempt(
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
    Ok((StatusCode::CREATED, Json(Scored { score })))
}

/// Body of `PUT /api/notes`.
#[derive(Deserialize)]
pub struct NoteInput {
    slug: String,
    text: String,
}

#[derive(Serialize)]
struct Note {
    note: Option<String>,
}

/// Saves your answer to a problem; empty text deletes it.
pub async fn save_note(
    State(state): State<Shared>,
    Json(input): Json<NoteInput>,
) -> ApiResult<impl IntoResponse> {
    let text = input.text.trim().to_owned();
    if text.chars().count() > MAX_NOTE_CHARS {
        return Err(ApiError::BadRequest(format!(
            "Notes are at most {MAX_NOTE_CHARS} characters"
        )));
    }
    let stored = text.clone();
    state
        .db_for(&input.slug, move |store, slug| {
            store.save_note(slug, &stored, now_ms())
        })
        .await?;
    let mut progress = state.progress.write();
    if text.is_empty() {
        progress.notes.remove(&input.slug);
        return Ok(Json(Note { note: None }));
    }
    progress.notes.insert(input.slug, text.clone());
    Ok(Json(Note { note: Some(text) }))
}

/// `?slug=two-sum` clears one problem, `?all=true` everything; anything else is rejected.
pub async fn reset_progress(
    State(state): State<Shared>,
    Query(params): Params,
) -> ApiResult<StatusCode> {
    match (param(&params, "slug"), param(&params, "all"), params.len()) {
        (Some(slug), None, 1) if !slug.is_empty() => {
            let slug = state
                .db_for(slug, |store, slug| {
                    store.delete_attempts(Some(slug))?;
                    Ok(slug.to_owned())
                })
                .await?;
            state.progress.write().clear(Some(&slug));
        }
        (None, Some("true"), 1) => {
            state.db(|store| store.delete_attempts(None)).await?;
            state.progress.write().clear(None);
        }
        _ => return Err(ApiError::BadRequest("Give either slug or all=true".into())),
    }
    Ok(StatusCode::NO_CONTENT)
}

/// `?company=&period=`: the rows of one list, in list order.
pub async fn problems(State(state): State<Shared>, Query(params): Params) -> Response {
    let list = state
        .content
        .list_id(param(&params, "company"), param(&params, "period"));
    let progress = state.progress.read();
    let rows = service::problem_rows(&state.content, list, &progress.states, now_ms());
    Json(&rows).into_response()
}

/// One problem's study card.
pub async fn problem(State(state): State<Shared>, Path(slug): Path<String>) -> ApiResult<Response> {
    let progress = state.progress.read();
    let note = progress.notes.get(&slug).cloned();
    let card = service::card(&state.content, &progress.states, &slug, note)?;
    Ok(Json(&card).into_response())
}

/// `?q=&limit=`: ranked search hits.
pub async fn search(State(state): State<Shared>, Query(params): Params) -> ApiResult<Response> {
    let q = param(&params, "q").unwrap_or_default();
    let limit = match param(&params, "limit") {
        Some(text) => text
            .parse::<usize>()
            .map_err(|_| ApiError::BadRequest("limit must be a number".into()))?,
        None => SEARCH_LIMIT,
    };
    let hits = state.content.search(q, limit.clamp(1, MAX_SEARCH_LIMIT));
    Ok(Json(&hits).into_response())
}

#[derive(Serialize)]
struct ReportPage<'a> {
    report: &'a ScoreReport,
    history: Vec<DailyScore>,
}

/// `?company=` (default google): the report for that company's 6-month list. The daily
/// history is the default company's.
pub async fn report(State(state): State<Shared>, Query(params): Params) -> ApiResult<Response> {
    let company = state.content.company_or_default(param(&params, "company"));
    let history = state.db(|store| store.daily_scores(HISTORY_DAYS)).await?;
    let mut progress = state.progress.write();
    let report = progress.report(&state.content, company, now_ms());
    Ok(Json(&ReportPage { report, history }).into_response())
}

#[derive(Serialize)]
struct Readiness {
    readiness: f64,
}

/// `?company=` (default google): that company's readiness alone.
pub async fn readiness(State(state): State<Shared>, Query(params): Params) -> Response {
    let company = state.content.company_or_default(param(&params, "company"));
    let mut progress = state.progress.write();
    let readiness = progress.report(&state.content, company, now_ms()).readiness;
    Json(Readiness { readiness }).into_response()
}
