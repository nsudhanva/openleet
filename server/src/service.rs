//! Pure read-side service logic: study cards, the deck, the problem table and new attempts
//! (port of the storage-free parts of `web/src/server/service.ts`).
//!
//! Nothing here touches the database: callers pass card states, notes and the clock in, and
//! serialize the returned structs as the JSON API responses.

use serde::{Deserialize, Serialize};

use crate::content::Content;
use crate::model::{Approach, AskedBy, Attempt, Difficulty, Grade, Problem};
use crate::scheduler::{
    CardList, CardState, CardStates, CardStatus, QueueFilter, card_status, queue_head,
};
use crate::scorer::score_topics;

/// A slug that names no problem (HTTP 404).
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
#[error("Unknown problem: {0}")]
pub struct UnknownProblem(pub String);

/// Input that breaks a limit (HTTP 400).
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
#[error("{0}")]
pub struct InvalidInput(pub &'static str);

/// One problem with everything the study page shows.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct StudyCard<'a> {
    /// The problem.
    pub problem: &'a Problem,
    /// Its worked approach, if one was written.
    pub approach: Option<&'a Approach>,
    /// Its Leitner state; `None` when never attempted.
    pub state: Option<CardState>,
    /// Your own answer, or `None` when you have not written one.
    pub note: Option<String>,
}

/// The next card to study in a set.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct StudyDeck<'a> {
    /// The pinned card, else the first in the queue; `None` when the set is empty.
    pub card: Option<StudyCard<'a>>,
    /// Cards left in the chosen set, including this one.
    pub remaining: usize,
    /// Every topic, most common first, for the guess picker.
    pub topics: &'a [String],
}

/// Every problem with its progress. Topics stay off so browsing does not spoil guesses.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ProblemRow<'a> {
    /// LeetCode number.
    pub id: u32,
    /// Slug.
    pub slug: &'a str,
    /// Title.
    pub title: &'a str,
    /// Difficulty.
    pub difficulty: Difficulty,
    /// Google frequency per period; `{}` for classic-only problems.
    pub asked: &'a AskedBy,
    /// Whether it needs LeetCode Premium.
    pub premium: bool,
    /// New, due or later.
    pub status: CardStatus,
    /// The list the last grade put it on.
    pub list: Option<CardList>,
    /// Graded attempts.
    pub reviews: u32,
    /// Topic score of the last graded attempt.
    pub last_score: Option<f64>,
    /// Time of the last attempt.
    pub last_at: Option<i64>,
    /// When it is next due.
    pub due: Option<i64>,
}

/// Query of the deck endpoint: a queue filter plus an optional pinned problem.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct DeckQuery {
    /// Which cards to study.
    pub filter: QueueFilter,
    /// Show this problem instead of the next one in the queue.
    pub slug: Option<String>,
}

impl DeckQuery {
    /// Builds a query from raw query-string values, as leniently as the study page's search
    /// schema: an unknown set falls back to "smart", an unknown period to "6m", an unknown
    /// difficulty and empty strings to no filter.
    #[must_use]
    pub fn from_params(
        set: Option<&str>,
        period: Option<&str>,
        topic: Option<&str>,
        difficulty: Option<&str>,
        slug: Option<&str>,
    ) -> Self {
        let non_empty = |v: Option<&str>| v.filter(|s| !s.is_empty()).map(str::to_owned);
        Self {
            filter: QueueFilter {
                set: set.and_then(|s| s.parse().ok()).unwrap_or_default(),
                period: Some(period.and_then(|p| p.parse().ok()).unwrap_or_default()),
                topic: non_empty(topic),
                difficulty: difficulty.and_then(|d| d.parse().ok()),
            },
            slug: non_empty(slug),
        }
    }
}

/// Body of `POST /api/attempts`.
#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
pub struct AttemptInput {
    /// The problem answered.
    pub slug: String,
    /// The learner's grade.
    pub grade: Grade,
    /// Topics guessed.
    #[serde(default)]
    pub guessed: Vec<String>,
    /// Hints opened.
    #[serde(default)]
    pub hints: u32,
}

/// Most topics one guess may list.
pub const MAX_GUESSED: usize = 200;
/// Most hints one attempt may report.
pub const MAX_HINTS: u32 = 10;

impl AttemptInput {
    /// Checks the limits of the attempt schema.
    ///
    /// # Errors
    /// When the slug is empty, more than [`MAX_GUESSED`] topics are guessed or more than
    /// [`MAX_HINTS`] hints are reported.
    pub fn validate(&self) -> Result<(), InvalidInput> {
        if self.slug.is_empty() {
            Err(InvalidInput("slug must not be empty"))
        } else if self.guessed.len() > MAX_GUESSED {
            Err(InvalidInput("too many guessed topics"))
        } else if self.hints > MAX_HINTS {
            Err(InvalidInput("hints must be at most 10"))
        } else {
            Ok(())
        }
    }
}

/// The problem with this slug, or [`UnknownProblem`].
///
/// # Errors
/// When no problem has this slug.
pub fn problem_of<'a>(content: &'a Content, slug: &str) -> Result<&'a Problem, UnknownProblem> {
    content
        .problem(slug)
        .ok_or_else(|| UnknownProblem(slug.to_owned()))
}

fn card_for<'a>(
    content: &'a Content,
    problem: &'a Problem,
    states: &CardStates,
    note: Option<String>,
) -> StudyCard<'a> {
    StudyCard {
        problem,
        approach: content.approach(&problem.slug),
        state: states.get(&problem.slug).copied(),
        note,
    }
}

/// One problem's study card. `note` is the learner's stored answer for `slug`.
///
/// # Errors
/// When no problem has this slug.
pub fn card<'a>(
    content: &'a Content,
    states: &CardStates,
    slug: &str,
    note: Option<String>,
) -> Result<StudyCard<'a>, UnknownProblem> {
    Ok(card_for(content, problem_of(content, slug)?, states, note))
}

/// The pinned problem when it exists, else the next card in the study set. `note_for` loads
/// the learner's answer for the chosen slug, and is called only when there is a card.
pub fn deck<'a>(
    content: &'a Content,
    states: &CardStates,
    query: &DeckQuery,
    now: i64,
    note_for: impl FnOnce(&str) -> Option<String>,
) -> StudyDeck<'a> {
    let (head, remaining) = queue_head(&content.problems, states, &query.filter, now);
    let pinned = query.slug.as_deref().and_then(|slug| content.problem(slug));
    StudyDeck {
        card: pinned
            .or(head)
            .map(|problem| card_for(content, problem, states, note_for(&problem.slug))),
        remaining,
        topics: &content.topics,
    }
}

/// Every problem with its progress, in list order.
#[must_use]
pub fn problem_rows<'a>(
    content: &'a Content,
    states: &CardStates,
    now: i64,
) -> Vec<ProblemRow<'a>> {
    content
        .problems
        .iter()
        .map(|p| {
            let state = states.get(&p.slug);
            ProblemRow {
                id: p.id,
                slug: &p.slug,
                title: &p.title,
                difficulty: p.difficulty,
                asked: &p.asked,
                premium: p.premium,
                status: card_status(state, now),
                list: state.and_then(|s| s.list),
                reviews: state.map_or(0, |s| s.reviews),
                last_score: state.and_then(|s| s.last_score),
                last_at: state.map(|s| s.last_at),
                due: state.map(|s| s.due),
            }
        })
        .collect()
}

/// The attempt to store for a validated answer: its topic score (none for a skip, whose
/// guesses are dropped).
///
/// # Errors
/// When no problem has the input's slug.
pub fn new_attempt(
    content: &Content,
    input: AttemptInput,
    now: i64,
) -> Result<Attempt, UnknownProblem> {
    let problem = problem_of(content, &input.slug)?;
    let skip = input.grade == Grade::Skip;
    let score = (!skip).then(|| score_topics(&input.guessed, &problem.topics).score);
    Ok(Attempt {
        slug: input.slug,
        at: now,
        grade: input.grade,
        guessed: if skip { Vec::new() } else { input.guessed },
        score,
        hints: input.hints,
    })
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use serde_json::json;

    use super::*;
    use crate::model::fixtures::{T0, attempt, problem};
    use crate::model::{Asked, Period};
    use crate::scheduler::{StudySet, card_states};

    fn content() -> Content {
        let mut classic = problem(3);
        classic.asked = AskedBy::default();
        let mut google = problem(1500);
        google.asked.months6 = Some(Asked {
            rank: 1,
            frequency: 50.0,
        });
        Content::new(vec![google, problem(2), classic], HashMap::new())
    }

    #[test]
    fn parses_deck_queries_leniently() {
        let q = DeckQuery::from_params(Some("bogus"), Some("1y"), Some(""), Some("Hard"), None);
        assert_eq!(q.filter.set, StudySet::Smart);
        assert_eq!(q.filter.period, Some(Period::Months6));
        assert_eq!(
            (q.filter.topic, q.filter.difficulty, q.slug),
            (None, Some(Difficulty::Hard), None)
        );
        let q = DeckQuery::from_params(Some("due"), Some("lc1000"), None, None, Some("p2"));
        assert_eq!(
            (q.filter.set, q.filter.period),
            (StudySet::Due, Some(Period::Lc1000))
        );
        assert_eq!(q.slug.as_deref(), Some("p2"));
    }

    #[test]
    fn deals_the_next_card_or_the_pinned_one() {
        let content = content();
        let states = CardStates::new();
        let mut asked = Vec::new();
        let six = DeckQuery::default();
        let six = DeckQuery {
            filter: QueueFilter {
                period: Some(Period::Months6),
                ..six.filter
            },
            ..six
        };
        let deck6 = deck(&content, &states, &six, T0, |slug| {
            asked.push(slug.to_owned());
            Some("my note".to_owned())
        });
        assert_eq!(deck6.remaining, 2);
        let card = deck6.card.expect("a card");
        assert_eq!(
            (card.problem.slug.as_str(), card.note.as_deref()),
            ("p1500", Some("my note"))
        );
        assert_eq!(asked, ["p1500"]);

        let lc = DeckQuery::from_params(None, Some("lc1000"), None, None, None);
        let deck_lc = deck(&content, &states, &lc, T0, |_| None);
        assert_eq!(deck_lc.remaining, 2);
        assert_eq!(deck_lc.card.map(|c| c.problem.id), Some(2));

        let pinned = DeckQuery::from_params(None, Some("30d"), None, None, Some("p3"));
        let deck_pinned = deck(&content, &states, &pinned, T0, |_| None);
        assert_eq!(
            (
                deck_pinned.remaining,
                deck_pinned.card.map(|c| c.problem.id)
            ),
            (0, Some(3))
        );
    }

    #[test]
    fn builds_problem_rows_with_progress() {
        let content = content();
        let states = card_states(&[attempt("p2", Grade::Again, T0)]);
        let rows = problem_rows(&content, &states, T0 + 1);
        let json = serde_json::to_value(&rows).expect("serialize");
        assert_eq!(
            json[1],
            json!({
                "id": 2, "slug": "p2", "title": "Problem 2", "difficulty": "Medium",
                "asked": {"6m": {"rank": 2, "frequency": 10.0}}, "premium": false,
                "status": "later", "list": "again", "reviews": 1, "lastScore": 1.0,
                "lastAt": T0, "due": T0 + 600_000,
            })
        );
        assert_eq!(json[2]["asked"], json!({}));
        assert_eq!(json[2]["status"], "new");
        assert_eq!(json[2]["lastAt"], serde_json::Value::Null);
    }

    #[test]
    fn serializes_cards_like_the_ts_service() {
        let content = content();
        let states = card_states(&[attempt("p2", Grade::Less, T0)]);
        let card = card(&content, &states, "p2", None).expect("known");
        let json = serde_json::to_value(&card).expect("serialize");
        assert_eq!(json["state"]["box"], 2);
        assert_eq!(json["state"]["lastGrade"], "less");
        assert_eq!(json["approach"], serde_json::Value::Null);
        assert!(matches!(
            super::card(&content, &states, "nope", None),
            Err(UnknownProblem(_))
        ));
    }

    #[test]
    fn scores_new_attempts() {
        let content = content();
        let input = |grade| AttemptInput {
            slug: "p2".into(),
            grade,
            guessed: vec!["Array".into()],
            hints: 1,
        };
        let good = new_attempt(&content, input(Grade::Good), T0).expect("known");
        assert_eq!(
            (good.score, good.guessed.len(), good.at),
            (Some(1.0), 1, T0)
        );
        let skip = new_attempt(&content, input(Grade::Skip), T0).expect("known");
        assert_eq!((skip.score, skip.guessed.len()), (None, 0));
        assert!(input(Grade::Good).validate().is_ok());
        assert!(
            AttemptInput {
                hints: 11,
                ..input(Grade::Good)
            }
            .validate()
            .is_err()
        );
        let unknown = AttemptInput {
            slug: "x".into(),
            ..input(Grade::Good)
        };
        assert!(new_attempt(&content, unknown, T0).is_err());
    }
}
