//! The learner's own problem lists: made, renamed, filled and emptied by hand, and walked by
//! practice plans like a company list (`list=<id>` on `GET /api/next` and `/api/problems`).

use std::collections::HashSet;

use axum::Json;
use axum::extract::{Path, State};
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use openleet::content::Content;
use openleet::lists::ProblemFilter;
use openleet::plan::{
    self, Marks, NextProblem, Plan, PlanOrder, PlanProgress, PlanStatus, PlanView,
};
use openleet::user_lists::{UserList, UserLists};

use super::plans::checked_name;
use crate::db::{ListWrite, MAX_LIST_PROBLEMS, MAX_LISTS};
use crate::error::{ApiError, ApiResult};
use crate::state::{AppState, Shared, now_ms, user_lists};

/// A list as the API shows it.
#[derive(Serialize)]
struct ListView<'a> {
    id: i64,
    name: &'a str,
    /// Its problems, in list order.
    slugs: &'a [String],
    /// The plan that walks it: its unsolved problems, in list order.
    plan: PlanView<'a>,
    progress: PlanProgress,
    /// The first problem still to do.
    next: Option<NextProblem<'a>>,
}

fn view<'a>(
    content: &'a Content,
    lists: &UserLists,
    list: &'a UserList,
    marks: Marks<'_>,
) -> ListView<'a> {
    let plan = Plan {
        list: content.list_id(None, None),
        user_list: Some(list.id),
        filter: ProblemFilter::default(),
        status: PlanStatus::default(),
        order: PlanOrder::default(),
    };
    let walked = plan::walk(content, lists, &plan, None, marks);
    ListView {
        id: list.id,
        name: &list.name,
        slugs: &list.slugs,
        plan: plan.labeled(content, lists),
        progress: walked.progress,
        next: walked.next,
    }
}

/// Every list, newest first.
pub async fn lists(State(state): State<Shared>) -> Response {
    let progress = state.progress.read();
    let views: Vec<ListView<'_>> = progress
        .lists
        .all()
        .iter()
        .map(|list| view(&state.content, &progress.lists, list, progress.marks()))
        .collect();
    Json(&views).into_response()
}

/// The list with `id`, as the API shows it, else a 404.
fn list_response(state: &Shared, id: i64, status: StatusCode) -> ApiResult<Response> {
    let progress = state.progress.read();
    let list = progress
        .lists
        .get(id)
        .ok_or_else(|| ApiError::NotFound(format!("No list {id}")))?;
    let body = Json(&view(
        &state.content,
        &progress.lists,
        list,
        progress.marks(),
    ));
    Ok((status, body).into_response())
}

/// A list's problems from the request: known slugs, each once (the first time it appears),
/// at most [`MAX_LIST_PROBLEMS`].
fn checked_slugs(content: &Content, slugs: Vec<String>) -> ApiResult<Vec<String>> {
    let mut seen = HashSet::new();
    let mut kept = Vec::with_capacity(slugs.len());
    for slug in slugs {
        if content.problem(&slug).is_none() {
            return Err(ApiError::BadRequest(format!("No problem {slug}")));
        }
        if seen.insert(slug.clone()) {
            kept.push(slug);
        }
    }
    if kept.len() > MAX_LIST_PROBLEMS {
        return Err(ApiError::BadRequest(format!(
            "A list holds at most {MAX_LIST_PROBLEMS} problems"
        )));
    }
    Ok(kept)
}

/// Rereads the lists after a write, so the memory matches the database.
fn reload(state: &AppState) -> anyhow::Result<()> {
    let lists = user_lists(&state.content, state.store.lists()?);
    state.progress.write().lists = lists;
    Ok(())
}

/// Body of `POST /api/lists`: a name and, optionally, its first problems.
#[derive(Deserialize)]
pub struct NewList {
    name: String,
    #[serde(default)]
    slugs: Vec<String>,
}

/// Makes a list.
pub async fn create_list(
    State(state): State<Shared>,
    Json(input): Json<NewList>,
) -> ApiResult<Response> {
    let name = checked_name(&input.name, "")?;
    let slugs = checked_slugs(&state.content, input.slugs)?;
    let written = state
        .update_progress(move |state| {
            let written = state.store.create_list(&name, &slugs, now_ms())?;
            if matches!(written, ListWrite::Done(_)) {
                reload(state)?;
            }
            Ok(written)
        })
        .await?;
    match written {
        ListWrite::Done(id) => list_response(&state, id, StatusCode::CREATED),
        ListWrite::TooMany => Err(ApiError::BadRequest(format!(
            "You can keep at most {MAX_LISTS} lists"
        ))),
        ListWrite::Missing => Err(ApiError::NotFound("No such list".into())),
    }
}

/// Body of `PATCH /api/lists/{id}`: a new name, the problems in their new order, or both.
#[derive(Deserialize)]
pub struct ListEdit {
    name: Option<String>,
    slugs: Option<Vec<String>>,
}

/// Renames a list or replaces its problems.
pub async fn edit_list(
    State(state): State<Shared>,
    Path(id): Path<i64>,
    Json(edit): Json<ListEdit>,
) -> ApiResult<Response> {
    let name = edit.name.map(|n| checked_name(&n, "")).transpose()?;
    let slugs = edit
        .slugs
        .map(|s| checked_slugs(&state.content, s))
        .transpose()?;
    let written = state
        .update_progress(move |state| {
            let written =
                state
                    .store
                    .change_list(id, name.as_deref(), slugs.as_deref(), now_ms())?;
            if matches!(written, ListWrite::Done(_)) {
                reload(state)?;
            }
            Ok(written)
        })
        .await?;
    match written {
        ListWrite::Done(id) => list_response(&state, id, StatusCode::OK),
        ListWrite::Missing | ListWrite::TooMany => Err(ApiError::NotFound(format!("No list {id}"))),
    }
}

/// Deletes a list.
pub async fn delete_list(
    State(state): State<Shared>,
    Path(id): Path<i64>,
) -> ApiResult<StatusCode> {
    let deleted = state
        .update_progress(move |state| {
            let deleted = state.store.delete_list(id)?;
            if deleted {
                reload(state)?;
            }
            Ok(deleted)
        })
        .await?;
    if deleted {
        Ok(StatusCode::NO_CONTENT)
    } else {
        Err(ApiError::NotFound(format!("No list {id}")))
    }
}

#[cfg(test)]
mod tests {
    use std::sync::Arc;

    use super::*;
    use crate::api::plans::next;
    use crate::api::testing::{json, query, state};
    use crate::db::testing::TempDir;

    fn slugs(names: &[&str]) -> Vec<String> {
        names.iter().map(|&s| s.to_owned()).collect()
    }

    async fn all(state: &Shared) -> serde_json::Value {
        json(lists(State(Arc::clone(state))).await).await
    }

    #[tokio::test]
    async fn lists_are_made_walked_edited_and_deleted() {
        let dir = TempDir::new("api-lists");
        let state = state(&dir);
        let made = create_list(
            State(Arc::clone(&state)),
            Json(NewList {
                name: "  Calculators ".into(),
                slugs: slugs(&["basic-calculator", "two-sum", "basic-calculator"]),
            }),
        )
        .await
        .expect("created");
        assert_eq!(made.status(), StatusCode::CREATED);
        let made = json(made).await;
        let id = made["id"].as_i64().expect("id");
        assert_eq!(made["name"], "Calculators");
        assert_eq!(
            made["slugs"],
            serde_json::json!(["basic-calculator", "two-sum"])
        );
        assert_eq!(made["plan"]["list"], id);
        assert_eq!(made["plan"]["label"], "Calculators · Unsolved");
        assert_eq!(made["next"]["slug"], "basic-calculator");
        assert_eq!(
            made["progress"],
            serde_json::json!({"solved": 0, "total": 2})
        );

        // A plan over the list walks it in its order.
        state.progress.write().coding.record(
            "basic-calculator",
            1,
            openleet_proto::Verdict::Accepted,
        );
        let id_text = id.to_string();
        let walked = json(
            next(
                State(Arc::clone(&state)),
                query(&[("list", &id_text), ("slug", "basic-calculator")]),
            )
            .await
            .expect("next"),
        )
        .await;
        assert_eq!(walked["next"]["slug"], "two-sum");
        assert_eq!(walked["progress"]["solved"], 1);

        let edited = edit_list(
            State(Arc::clone(&state)),
            Path(id),
            Json(ListEdit {
                name: Some("Stack drills".into()),
                slugs: Some(slugs(&["two-sum", "basic-calculator-ii"])),
            }),
        )
        .await
        .expect("edited");
        let edited = json(edited).await;
        assert_eq!(edited["name"], "Stack drills");
        assert_eq!(
            edited["slugs"],
            serde_json::json!(["two-sum", "basic-calculator-ii"])
        );
        assert_eq!(all(&state).await.as_array().map(Vec::len), Some(1));

        // Unknown problems, blank names and unknown lists are refused.
        let unknown = edit_list(
            State(Arc::clone(&state)),
            Path(id),
            Json(ListEdit {
                name: None,
                slugs: Some(slugs(&["no-such-problem"])),
            }),
        )
        .await;
        assert!(matches!(unknown, Err(ApiError::BadRequest(_))));
        let blank = create_list(
            State(Arc::clone(&state)),
            Json(NewList {
                name: "  ".into(),
                slugs: Vec::new(),
            }),
        )
        .await;
        assert!(matches!(blank, Err(ApiError::BadRequest(_))));
        let missing = edit_list(
            State(Arc::clone(&state)),
            Path(id + 1),
            Json(ListEdit {
                name: Some("x".into()),
                slugs: None,
            }),
        )
        .await;
        assert!(matches!(missing, Err(ApiError::NotFound(_))));

        assert_eq!(
            delete_list(State(Arc::clone(&state)), Path(id))
                .await
                .expect("deleted"),
            StatusCode::NO_CONTENT
        );
        assert!(matches!(
            delete_list(State(Arc::clone(&state)), Path(id)).await,
            Err(ApiError::NotFound(_))
        ));
        assert_eq!(all(&state).await, serde_json::json!([]));
        // The table of a deleted list is empty, not an error.
        let rows =
            crate::api::study::problems(State(Arc::clone(&state)), query(&[("list", &id_text)]))
                .await;
        assert_eq!(json(rows).await, serde_json::json!([]));
    }
}
