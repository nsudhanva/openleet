//! Practice plan endpoints: the next problem of a plan, and the plans the learner used
//! (recent and pinned).

use axum::Json;
use axum::extract::{Path, Query, State};
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use openleet::content::Content;
use openleet::plan::{self, Marks, NextProblem, Plan, PlanProgress, PlanView};
use openleet::service::{ProblemParams, ProblemQuery};

use super::{Params, param};
use crate::db::{Changed, MAX_PINNED_PLANS, PlanChange, PlanKey, SavedPlan};
use crate::error::{ApiError, ApiResult};
use crate::state::{Shared, now_ms};

/// Longest plan name, in characters.
const MAX_NAME_CHARS: usize = 60;

/// A plan from query or body values, leniently (see [`ProblemQuery::parse`]).
fn parse_plan(content: &Content, params: &ProblemParams<'_>) -> Plan {
    ProblemQuery::parse(content, params).plan()
}

/// `?slug=&company=&period=&topic=&difficulty=&status=&order=`: the plan's next problem after
/// `slug` (from the start without one), its progress and, from `slug`, the pivots. All from
/// memory; an unknown slug is a 404.
pub async fn next(State(state): State<Shared>, Query(params): Params) -> ApiResult<Response> {
    let content = &state.content;
    let current = match param(&params, "slug").filter(|s| !s.is_empty()) {
        Some(slug) => Some(state.problem(slug)?),
        None => None,
    };
    let plan = parse_plan(
        content,
        &ProblemParams {
            company: param(&params, "company"),
            period: param(&params, "period"),
            topic: param(&params, "topic"),
            difficulty: param(&params, "difficulty"),
            status: param(&params, "status"),
            order: param(&params, "order"),
            q: None,
        },
    );
    let (progress, report) = match current {
        Some(_) => {
            let (progress, report) = state.report(plan.list.company, now_ms());
            (progress, Some(report))
        }
        None => (state.progress.read(), None),
    };
    // The topic you name least, as the progress page lists them: rated on every graded card,
    // so any company's report names the same one.
    let weakest = report
        .as_ref()
        .and_then(|r| r.topics.first())
        .map(|t| t.topic.as_str());
    let page = plan::next_page(content, &plan, current, progress.marks(), weakest);
    Ok(Json(&page).into_response())
}

/// A stored plan as the API shows it.
#[derive(Serialize)]
struct PlanEntry<'a> {
    id: i64,
    /// The learner's name; `None` shows the label.
    name: Option<&'a str>,
    pinned: bool,
    plan: PlanView<'a>,
    progress: PlanProgress,
    /// The first problem still to do.
    next: Option<NextProblem<'a>>,
}

fn entry<'a>(content: &'a Content, saved: &'a SavedPlan, marks: Marks<'_>) -> PlanEntry<'a> {
    let plan = parse_plan(
        content,
        &ProblemParams {
            company: Some(&saved.company),
            period: Some(&saved.period),
            topic: saved.topic.as_deref(),
            difficulty: saved.difficulty.as_deref(),
            status: Some(&saved.status),
            order: Some(&saved.order),
            q: None,
        },
    );
    let walked = plan::walk(content, &plan, None, marks);
    PlanEntry {
        id: saved.id,
        name: saved.name.as_deref(),
        pinned: saved.pinned,
        plan: plan.labeled(content),
        progress: walked.progress,
        next: walked.next,
    }
}

/// Pinned plans first, then the recent ones, last used first.
pub async fn plans(State(state): State<Shared>) -> Response {
    let progress = state.progress.read();
    let entries: Vec<PlanEntry<'_>> = progress
        .plans
        .iter()
        .map(|saved| entry(&state.content, saved, progress.marks()))
        .collect();
    Json(&entries).into_response()
}

/// The stored plan with `id`, as the API shows it, else a 404.
fn plan_response(state: &Shared, id: i64) -> ApiResult<Response> {
    let progress = state.progress.read();
    let saved = progress
        .plans
        .iter()
        .find(|p| p.id == id)
        .ok_or_else(|| ApiError::NotFound(format!("No plan {id}")))?;
    Ok(Json(&entry(&state.content, saved, progress.marks())).into_response())
}

/// Body of `PUT /api/plans`: a plan's values, parsed like the query of `GET /api/next`.
#[derive(Deserialize)]
pub struct PlanInput {
    company: Option<String>,
    period: Option<String>,
    topic: Option<String>,
    difficulty: Option<String>,
    status: Option<String>,
    order: Option<String>,
}

/// Records that a plan was used: the same plan keeps its row (and name and pin), a new one
/// joins the recent plans, the oldest of which may go. Returns the plan.
pub async fn use_plan(
    State(state): State<Shared>,
    Json(input): Json<PlanInput>,
) -> ApiResult<Response> {
    let plan = parse_plan(
        &state.content,
        &ProblemParams {
            company: input.company.as_deref(),
            period: input.period.as_deref(),
            topic: input.topic.as_deref(),
            difficulty: input.difficulty.as_deref(),
            status: input.status.as_deref(),
            order: input.order.as_deref(),
            q: None,
        },
    );
    let id = state
        .update_progress(move |state| {
            let view = plan.view(&state.content);
            let key = PlanKey {
                company: view.company,
                period: view.period.as_str(),
                topic: view.topic,
                difficulty: view.difficulty.map(|d| d.as_str()),
                status: view.status.as_str(),
                order: view.order.as_str(),
            };
            let id = state.store.use_plan(&key, now_ms())?;
            let plans = state.store.plans()?;
            state.progress.write().plans = plans;
            Ok(id)
        })
        .await?;
    plan_response(&state, id)
}

/// Body of `PATCH /api/plans/{id}`: a new name (`null` for none, so the label shows), a pin,
/// or both.
#[derive(Deserialize)]
pub struct PlanEdit {
    #[serde(default, deserialize_with = "openleet_proto::present")]
    name: Option<Option<String>>,
    pinned: Option<bool>,
}

impl PlanEdit {
    /// The change, with the name trimmed.
    ///
    /// # Errors
    /// When the name is blank or longer than [`MAX_NAME_CHARS`].
    fn change(self) -> ApiResult<PlanChange> {
        let name = match self.name {
            Some(Some(name)) => {
                let name = name.trim();
                if name.is_empty() {
                    return Err(ApiError::BadRequest(
                        "A name needs some text; use null to drop it".into(),
                    ));
                }
                if name.chars().count() > MAX_NAME_CHARS {
                    return Err(ApiError::BadRequest(format!(
                        "Names are at most {MAX_NAME_CHARS} characters"
                    )));
                }
                Some(Some(name.to_owned()))
            }
            other => other,
        };
        Ok(PlanChange {
            name,
            pinned: self.pinned,
        })
    }
}

/// Renames, pins or unpins a plan.
pub async fn edit_plan(
    State(state): State<Shared>,
    Path(id): Path<i64>,
    Json(edit): Json<PlanEdit>,
) -> ApiResult<Response> {
    let change = edit.change()?;
    let changed = state
        .update_progress(move |state| {
            let changed = state.store.change_plan(id, &change, now_ms())?;
            if changed == Changed::Done {
                let plans = state.store.plans()?;
                state.progress.write().plans = plans;
            }
            Ok(changed)
        })
        .await?;
    match changed {
        Changed::Done => plan_response(&state, id),
        Changed::Missing => Err(ApiError::NotFound(format!("No plan {id}"))),
        Changed::TooManyPinned => Err(ApiError::BadRequest(format!(
            "At most {MAX_PINNED_PLANS} plans can be pinned"
        ))),
    }
}

/// Forgets a plan.
pub async fn delete_plan(
    State(state): State<Shared>,
    Path(id): Path<i64>,
) -> ApiResult<StatusCode> {
    let deleted = state
        .update_progress(move |state| {
            let deleted = state.store.delete_plan(id)?;
            if deleted {
                state.progress.write().plans.retain(|p| p.id != id);
            }
            Ok(deleted)
        })
        .await?;
    if deleted {
        Ok(StatusCode::NO_CONTENT)
    } else {
        Err(ApiError::NotFound(format!("No plan {id}")))
    }
}

#[cfg(test)]
mod tests {
    use std::sync::Arc;

    use super::*;
    use crate::api::testing::{json, query, state};
    use crate::db::testing::TempDir;

    async fn next_of(state: &Shared, pairs: &[(&str, &str)]) -> serde_json::Value {
        json(
            next(State(Arc::clone(state)), query(pairs))
                .await
                .expect("next"),
        )
        .await
    }

    #[tokio::test]
    async fn next_walks_the_plan_from_memory_without_spoiling_topics() {
        let dir = TempDir::new("api-next");
        let state = state(&dir);
        let first = next_of(&state, &[]).await;
        assert_eq!(first["plan"]["label"], "Google · 6 months · Unsolved");
        assert_eq!(first["next"]["slug"], "two-sum");
        assert_eq!(first["next"]["rank"], 1);
        assert!(first["next"].get("topics").is_none());
        assert_eq!(first["pivots"], serde_json::json!([]));
        let total = first["progress"]["total"].as_u64().expect("total");
        assert!(total > 100);

        state
            .progress
            .write()
            .coding
            .record("two-sum", 1, openleet_proto::Verdict::Accepted);
        let after = next_of(&state, &[("slug", "two-sum")]).await;
        assert_ne!(after["next"]["slug"], "two-sum");
        assert_eq!(after["progress"]["solved"], 1);
        let pivots = after["pivots"].as_array().expect("pivots");
        assert!(!pivots.is_empty() && pivots.len() <= plan::MAX_PIVOTS);
        assert!(
            pivots
                .iter()
                .all(|p| p["next"]["slug"] != after["next"]["slug"])
        );
        assert!(pivots.iter().any(|p| p["kind"] == "topic"));
        // Each pivot is another plan: here Two Sum's topics (its Medium pivot would go on to
        // Add Two Numbers, the plan's own next).
        assert!(pivots.iter().all(|p| p["plan"] != after["plan"]));
        assert_eq!(after["next"]["slug"], "add-two-numbers");
        assert!(pivots.iter().all(|p| p["kind"] == "topic"), "{pivots:?}");
        // Unknown values fall back to the defaults; an unknown problem is a 404.
        let lenient = next_of(&state, &[("status", "x"), ("order", "y"), ("period", "1y")]).await;
        assert_eq!(lenient["plan"], first["plan"]);
        let unknown = next(
            State(Arc::clone(&state)),
            query(&[("slug", "no-such-problem")]),
        )
        .await;
        assert!(matches!(unknown, Err(ApiError::NotFound(_))));
        let numbered = next_of(&state, &[("period", "lc1000"), ("order", "number")]).await;
        assert_eq!(numbered["next"]["id"], 2, "two-sum (1) is solved");
    }

    fn input(topic: Option<&str>) -> PlanInput {
        PlanInput {
            company: Some("meta".into()),
            period: Some("3m".into()),
            topic: topic.map(str::to_owned),
            difficulty: None,
            status: None,
            order: Some("nonsense".into()),
        }
    }

    #[tokio::test]
    async fn plans_are_remembered_once_renamed_pinned_and_removed() {
        let dir = TempDir::new("api-plans");
        let state = state(&dir);
        let used = |input| async {
            json(
                use_plan(State(Arc::clone(&state)), Json(input))
                    .await
                    .expect("used"),
            )
            .await
        };
        let first = used(input(None)).await;
        assert_eq!(first["plan"]["label"], "Meta · 3 months · Unsolved");
        assert_eq!(first["plan"]["order"], "rank");
        assert_eq!(
            (&first["name"], &first["pinned"]),
            (&serde_json::Value::Null, &false.into())
        );
        let again = used(input(None)).await;
        assert_eq!(again["id"], first["id"]);
        let graph = used(input(Some("Graph Theory"))).await;
        assert_ne!(graph["id"], first["id"]);
        let list = json(plans(State(Arc::clone(&state))).await).await;
        assert_eq!(list.as_array().map(Vec::len), Some(2));
        assert_eq!(list[0]["id"], graph["id"], "last used first");
        assert_eq!(state.progress.read().plans, state.store.plans().unwrap());

        let id = first["id"].as_i64().expect("id");
        let edit = |body: serde_json::Value| {
            let state = Arc::clone(&state);
            async move {
                let edit: PlanEdit = serde_json::from_value(body).expect("edit");
                edit_plan(State(state), Path(id), Json(edit)).await
            }
        };
        let named = json(
            edit(serde_json::json!({"name": "  Meta warm-up ", "pinned": true}))
                .await
                .expect("named"),
        )
        .await;
        assert_eq!(
            (&named["name"], &named["pinned"]),
            (&"Meta warm-up".into(), &true.into())
        );
        let list = json(plans(State(Arc::clone(&state))).await).await;
        assert_eq!(list[0]["id"], id, "pinned first");
        for bad in [
            serde_json::json!({"name": "   "}),
            serde_json::json!({"name": "x".repeat(61)}),
        ] {
            assert!(matches!(edit(bad).await, Err(ApiError::BadRequest(_))));
        }
        // Left out keeps the name; null drops it.
        let kept = json(
            edit(serde_json::json!({"pinned": true}))
                .await
                .expect("kept"),
        )
        .await;
        assert_eq!(kept["name"], "Meta warm-up");
        let cleared = json(
            edit(serde_json::json!({"name": null}))
                .await
                .expect("cleared"),
        )
        .await;
        assert_eq!(cleared["name"], serde_json::Value::Null);

        assert_eq!(
            delete_plan(State(Arc::clone(&state)), Path(id))
                .await
                .expect("deleted"),
            StatusCode::NO_CONTENT
        );
        assert!(matches!(
            delete_plan(State(Arc::clone(&state)), Path(id)).await,
            Err(ApiError::NotFound(_))
        ));
        let missing: PlanEdit =
            serde_json::from_value(serde_json::json!({"pinned": true})).expect("edit");
        assert!(matches!(
            edit_plan(State(Arc::clone(&state)), Path(id), Json(missing)).await,
            Err(ApiError::NotFound(_))
        ));
        assert_eq!(state.progress.read().plans.len(), 1);
    }
}
