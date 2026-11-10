//! Flashcard endpoints: companies, deck, attempts, notes, progress, problems, search, report.

use axum::Json;
use axum::body::Bytes;
use axum::extract::{Path, Query, State};
use axum::http::{HeaderMap, HeaderValue, StatusCode, header};
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use openleet::content::Content;
use openleet::scorer::ScoreReport;
use openleet::service::{self, AttemptInput, DeckParams, DeckQuery, ProblemParams, ProblemQuery};

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

/// JSON that changes only with the data: sent with its `ETag` and `no-cache`, so clients
/// revalidate and get a 304 when they already hold it.
fn revalidated(headers: &HeaderMap, body: Bytes, etag: HeaderValue) -> Response {
    let fresh = headers.get(header::IF_NONE_MATCH) == Some(&etag);
    let head = [
        (
            header::CONTENT_TYPE,
            HeaderValue::from_static("application/json"),
        ),
        (header::CACHE_CONTROL, HeaderValue::from_static("no-cache")),
        (header::ETAG, etag),
    ];
    if fresh {
        (StatusCode::NOT_MODIFIED, head).into_response()
    } else {
        (head, body).into_response()
    }
}

/// Companies change only with the data, so clients revalidate with the `ETag`.
pub async fn companies(State(state): State<Shared>, headers: HeaderMap) -> Response {
    let (body, etag) = &state.companies;
    revalidated(&headers, body.clone(), etag.clone())
}

/// `?company=&period=&difficulty=`: the topics of that list's problems (of that difficulty)
/// with their counts, most first. Counts depend only on the data and the query, so the
/// response carries an `ETag`.
pub async fn topics(
    State(state): State<Shared>,
    headers: HeaderMap,
    Query(params): Params,
) -> ApiResult<Response> {
    let content = &state.content;
    let list = content.list_id(param(&params, "company"), param(&params, "period"));
    let difficulty = content
        .problem_filter(None, param(&params, "difficulty"))
        .difficulty;
    let body = serde_json::to_vec(&content.topic_counts(list, difficulty))
        .map_err(|e| ApiError::Internal(e.into()))?;
    let etag = HeaderValue::from_str(&fingerprint::etag(&body))
        .map_err(|e| ApiError::Internal(e.into()))?;
    Ok(revalidated(&headers, body.into(), etag))
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

/// `?company=&period=&topic=&difficulty=&q=`: the rows of one list that pass the filter, in
/// list order, or best match first with a search.
pub async fn problems(State(state): State<Shared>, Query(params): Params) -> Response {
    let query = ProblemQuery::parse(
        &state.content,
        &ProblemParams {
            company: param(&params, "company"),
            period: param(&params, "period"),
            topic: param(&params, "topic"),
            difficulty: param(&params, "difficulty"),
            q: param(&params, "q"),
        },
    );
    let progress = state.progress.read();
    let rows = service::problem_rows(&state.content, &query, &progress.states, now_ms());
    Json(&rows).into_response()
}

/// One problem's study card.
pub async fn problem(State(state): State<Shared>, Path(slug): Path<String>) -> ApiResult<Response> {
    let progress = state.progress.read();
    let note = progress.notes.get(&slug).cloned();
    let card = service::card(&state.content, &progress.states, &slug, note)?;
    Ok(Json(&card).into_response())
}

/// `?q=&limit=`: ranked search hits. `q` is what the endpoint is for, so leaving it out (or
/// blank) is a 400, like a bad `limit`; the list filters elsewhere are lenient instead.
pub async fn search(State(state): State<Shared>, Query(params): Params) -> ApiResult<Response> {
    let q = param(&params, "q")
        .map(str::trim)
        .filter(|q| !q.is_empty())
        .ok_or_else(|| ApiError::BadRequest("q is required".into()))?;
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

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::path::Path;
    use std::sync::Arc;

    use super::*;
    use crate::db::testing::TempDir;
    use crate::state::test_state_with;

    fn state(dir: &TempDir) -> Shared {
        let data = Path::new(env!("CARGO_MANIFEST_DIR")).join("../data");
        let content = Content::load(&data.join("problems.json"), &data.join("approaches.json"))
            .expect("load the problems file");
        test_state_with(dir.root(), "tcp://127.0.0.1:1", content)
    }

    fn query(pairs: &[(&str, &str)]) -> Params {
        Query(
            pairs
                .iter()
                .map(|&(k, v)| (k.to_owned(), v.to_owned()))
                .collect::<HashMap<_, _>>(),
        )
    }

    async fn json(response: Response) -> serde_json::Value {
        let body = axum::body::to_bytes(response.into_body(), 1 << 24)
            .await
            .expect("body");
        serde_json::from_slice(&body).expect("json")
    }

    async fn topic_list(state: &Shared, pairs: &[(&str, &str)]) -> Vec<(String, u64)> {
        let response = topics(State(Arc::clone(state)), HeaderMap::new(), query(pairs))
            .await
            .expect("topics");
        json(response)
            .await
            .as_array()
            .expect("array")
            .iter()
            .map(|t| {
                (
                    t["topic"].as_str().expect("topic").to_owned(),
                    t["problems"].as_u64().expect("count"),
                )
            })
            .collect()
    }

    async fn rows(state: &Shared, pairs: &[(&str, &str)]) -> Vec<serde_json::Value> {
        let response = problems(State(Arc::clone(state)), query(pairs)).await;
        json(response).await.as_array().expect("array").clone()
    }

    #[tokio::test]
    async fn topics_count_the_list_most_first_and_revalidate() {
        let dir = TempDir::new("api-topics");
        let state = state(&dir);
        let all = topic_list(&state, &[]).await;
        assert_eq!(all[0].0, "Array");
        assert!(
            all.windows(2)
                .all(|w| w[0].1 > w[1].1 || (w[0].1 == w[1].1 && w[0].0 < w[1].0))
        );
        assert!(all.iter().all(|t| t.1 > 0));
        let total = rows(&state, &[]).await.len();
        assert_eq!(
            all[0].1,
            rows(&state, &[("topic", "Array")]).await.len() as u64
        );
        assert!(all[0].1 < total as u64);

        // After the difficulty filter: every count shrinks or stays.
        let hard = topic_list(&state, &[("difficulty", "Hard")]).await;
        for (topic, count) in &hard {
            let full = all.iter().find(|t| &t.0 == topic).expect("listed").1;
            assert!(*count <= full, "{topic}");
        }
        let graph = hard
            .iter()
            .find(|t| t.0 == "Graph Theory")
            .expect("Graph Theory")
            .1;
        let filtered = rows(&state, &[("topic", "Graph Theory"), ("difficulty", "Hard")]).await;
        assert_eq!(filtered.len() as u64, graph);
        assert!(filtered.iter().all(|r| r["difficulty"] == "Hard"));
        assert!(filtered.iter().all(|r| r.get("topics").is_none()));
        // An unknown difficulty is no filter.
        assert_eq!(
            topic_list(&state, &[("difficulty", "Impossible")]).await,
            all
        );

        // The ETag answers a revalidation with 304.
        let first = topics(State(Arc::clone(&state)), HeaderMap::new(), query(&[]))
            .await
            .expect("topics");
        assert_eq!(first.headers()[header::CACHE_CONTROL], "no-cache");
        let etag = first.headers()[header::ETAG].clone();
        let mut headers = HeaderMap::new();
        headers.insert(header::IF_NONE_MATCH, etag);
        let again = topics(State(Arc::clone(&state)), headers, query(&[]))
            .await
            .expect("topics");
        assert_eq!(again.status(), StatusCode::NOT_MODIFIED);
    }

    #[tokio::test]
    async fn problems_compose_list_filters_and_search() {
        let dir = TempDir::new("api-problems");
        let state = state(&dir);
        let all = rows(&state, &[]).await;
        let medium = rows(&state, &[("difficulty", "Medium")]).await;
        assert!(!medium.is_empty() && medium.len() < all.len());
        // Filtering keeps list order.
        let ranks: Vec<_> = medium.iter().map(|r| r["rank"].as_u64()).collect();
        assert!(ranks.windows(2).all(|w| w[0] <= w[1]));
        // Unknown values filter nothing.
        assert_eq!(
            rows(&state, &[("topic", "Nope"), ("difficulty", "x")])
                .await
                .len(),
            all.len()
        );

        let hits = rows(
            &state,
            &[("q", "two sum"), ("company", "meta"), ("period", "all")],
        )
        .await;
        assert_eq!(hits[0]["slug"], "two-sum");
        let none = rows(&state, &[("q", "two sum"), ("difficulty", "Hard")]).await;
        assert!(
            none.iter()
                .all(|r| r["slug"] != "two-sum" && r["difficulty"] == "Hard")
        );
        let lc = rows(
            &state,
            &[("period", "lc1000"), ("topic", "Trie"), ("q", "word")],
        )
        .await;
        assert_ne!(lc.len(), 0);
        assert!(lc.iter().all(|r| r["id"].as_u64() <= Some(1000)));
    }

    #[tokio::test]
    async fn search_needs_a_query() {
        let dir = TempDir::new("api-search");
        let state = state(&dir);
        let hits = search(State(Arc::clone(&state)), query(&[("q", " two sum ")]))
            .await
            .expect("hits");
        assert_eq!(json(hits).await[0]["slug"], "two-sum");
        for pairs in [&[][..], &[("q", "  ")], &[("q", "x"), ("limit", "many")]] {
            let error = search(State(Arc::clone(&state)), query(pairs)).await;
            assert!(matches!(error, Err(ApiError::BadRequest(_))), "{pairs:?}");
        }
    }
}
