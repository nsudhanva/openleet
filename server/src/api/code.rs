//! Coding endpoints: problem code info, drafts, run, submit and submission history.

use axum::Json;
use axum::extract::{Path, Query, State};
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use openleet_proto::Verdict;

use super::{Params, param};
use crate::db::{NewSubmission, Store, TestRow};
use crate::error::{ApiError, ApiResult};
use crate::judge::{self, Entry, Shown, show_expected, show_input};
use crate::state::{Shared, now_ms};

const SUBMISSIONS_SHOWN: usize = 50;

/// A problem's tests, in order (404 for an unknown problem).
async fn tests(state: &Shared, slug: &str) -> ApiResult<Vec<TestRow>> {
    state.db_for(slug, Store::tests).await
}

/// The judge entry of a problem that can be judged, else a 400 (or 404 if unknown).
fn judged<'a>(state: &'a Shared, slug: &str) -> ApiResult<&'a Entry> {
    state.problem(slug)?;
    state
        .judge
        .entry(slug)
        .filter(|e| e.supported)
        .ok_or_else(|| ApiError::BadRequest("This problem cannot be judged yet".into()))
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct JudgeInfo<'a> {
    supported: bool,
    reason: Option<&'a str>,
    examples: u32,
    hidden: u32,
    stress: u32,
    time_limit_ms: Option<u32>,
}

#[derive(Serialize)]
struct CodeInfo<'a> {
    slug: &'a str,
    starter: Option<&'a str>,
    draft: Option<String>,
    previous: Option<String>,
    judge: JudgeInfo<'a>,
    examples: Vec<Shown>,
    solved: bool,
}

/// Starter, draft, judge support and the examples shown above the editor.
pub async fn code_info(
    State(state): State<Shared>,
    Path(slug): Path<String>,
) -> ApiResult<Response> {
    let tests = tests(&state, &slug).await?;
    let draft = state.db_for(&slug, Store::draft).await?;
    let entry = state.judge.entry(&slug);
    let examples: Vec<Shown> = entry.map_or_else(Vec::new, |entry| {
        tests
            .iter()
            .filter(|t| t.is_example())
            .map(|t| Shown {
                input: show_input(entry, &t.test),
                expected: show_expected(&t.expected),
            })
            .collect()
    });
    let supported = entry.is_some_and(|e| e.supported) && !tests.is_empty();
    let reason = match entry {
        Some(e) if !e.supported => e.reason.as_deref(),
        None => Some("This problem cannot be judged yet."),
        _ if tests.is_empty() => Some("This problem has no tests yet."),
        _ => None,
    };
    let counts = entry.map(|e| &e.tests);
    let info = CodeInfo {
        slug: &slug,
        starter: entry.and_then(|e| e.starter.as_deref()),
        draft: draft.code,
        previous: draft.previous,
        judge: JudgeInfo {
            supported,
            reason,
            examples: counts.map_or(0, |c| c.example),
            hidden: counts.map_or(0, |c| c.hidden),
            stress: counts.map_or(0, |c| c.stress),
            time_limit_ms: entry.filter(|_| supported).map(Entry::limit_ms),
        },
        examples,
        solved: state.progress.read().coding.solved(&slug),
    };
    Ok(Json(&info).into_response())
}

/// Body of the draft endpoints: the editor's code for a problem.
#[derive(Deserialize)]
pub struct DraftInput {
    slug: String,
    code: String,
}

/// Saves the editor's code ('' for "back to the starter").
pub async fn save_draft(
    State(state): State<Shared>,
    Json(input): Json<DraftInput>,
) -> ApiResult<StatusCode> {
    judge::check_code_size(&input.code)?;
    state
        .db_for(&input.slug, move |store, slug| {
            store.save_draft(slug, &input.code, now_ms())
        })
        .await?;
    Ok(StatusCode::NO_CONTENT)
}

/// Reset to the starter; the editor's code becomes the previous version.
pub async fn reset_draft(
    State(state): State<Shared>,
    Json(input): Json<DraftInput>,
) -> ApiResult<impl IntoResponse> {
    judge::check_code_size(&input.code)?;
    let draft = state
        .db_for(&input.slug, move |store, slug| {
            store.reset_draft(slug, &input.code, now_ms())
        })
        .await?;
    Ok(Json(draft))
}

/// Bring back the previous version; the editor's code becomes the previous one.
pub async fn restore_draft(
    State(state): State<Shared>,
    Json(input): Json<DraftInput>,
) -> ApiResult<impl IntoResponse> {
    judge::check_code_size(&input.code)?;
    state
        .db_for(&input.slug, move |store, slug| {
            store.restore_draft(slug, &input.code, now_ms())
        })
        .await?
        .map(Json)
        .ok_or_else(|| ApiError::BadRequest("There is no previous version to restore".into()))
}

/// Body of `POST /api/run`; `input` holds custom cases, one JSON value per line.
#[derive(Deserialize)]
pub struct RunInput {
    slug: String,
    code: String,
    input: Option<String>,
}

/// Runs the examples, or the custom cases in `input`.
pub async fn run(
    State(state): State<Shared>,
    Json(input): Json<RunInput>,
) -> ApiResult<impl IntoResponse> {
    let entry = judged(&state, &input.slug)?;
    let mut examples = tests(&state, &input.slug).await?;
    examples.retain(TestRow::is_example);
    let custom = input
        .input
        .as_deref()
        .filter(|text| !text.trim().is_empty());
    Ok(Json(
        state
            .judge
            .run(entry, &examples, &input.code, custom)
            .await?,
    ))
}

/// Body of `POST /api/submit`.
#[derive(Deserialize)]
pub struct SubmitInput {
    slug: String,
    code: String,
}

/// Judges every test and records the submission.
pub async fn submit(
    State(state): State<Shared>,
    Json(input): Json<SubmitInput>,
) -> ApiResult<impl IntoResponse> {
    let entry = judged(&state, &input.slug)?;
    let tests = tests(&state, &input.slug).await?;
    let (outcome, limit_ms) = state.judge.submit(entry, &tests, &input.code).await?;
    if outcome.rerun {
        tracing::info!(
            "judge: {} ran twice, the machine slowed to {:.1}x the reference",
            input.slug,
            outcome.slowdown
        );
    }
    let approach = state.content.approach(&input.slug);
    let mut result = judge::submit_result(entry, &tests, &outcome, limit_ms, approach);
    // A fault of the judge is not the solution's: report it without recording it.
    if outcome.verdict == Verdict::InternalError {
        return Ok(Json(result));
    }
    let detail =
        serde_json::to_string(&result.detail()).map_err(|e| ApiError::Internal(e.into()))?;
    let (verdict, passed, total, cpu_ms) =
        (result.verdict, result.passed, result.total, result.cpu_ms);
    let code = input.code;
    result.id = state
        .update_progress(move |state| {
            let at = now_ms();
            let id = state.store.insert_submission(&NewSubmission {
                slug: &input.slug,
                at,
                code: &code,
                verdict,
                passed,
                total,
                cpu_ms,
                detail: &detail,
            })?;
            state
                .progress
                .write()
                .coding
                .record(&input.slug, at, outcome.verdict);
            Ok(id)
        })
        .await?;
    Ok(Json(result))
}

/// `?slug=`: a problem's submissions, newest first.
pub async fn submissions(
    State(state): State<Shared>,
    Query(params): Params,
) -> ApiResult<impl IntoResponse> {
    let slug =
        param(&params, "slug").ok_or_else(|| ApiError::BadRequest("slug is required".into()))?;
    let rows = state
        .db_for(slug, |store, slug| {
            store.submissions(slug, SUBMISSIONS_SHOWN)
        })
        .await?;
    Ok(Json(rows))
}

/// One submission with its code and result.
pub async fn submission(
    State(state): State<Shared>,
    Path(id): Path<i64>,
) -> ApiResult<impl IntoResponse> {
    state
        .db(move |store| store.submission(id))
        .await?
        .map(Json)
        .ok_or_else(|| ApiError::NotFound(format!("No submission {id}")))
}
