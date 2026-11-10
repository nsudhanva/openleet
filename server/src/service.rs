//! Pure read-side service logic: study cards, the deck, the problem table and new attempts.
//!
//! Nothing here touches the database: callers pass card states, notes and the clock in, and
//! serialize the returned structs as the JSON API responses.

use serde::{Deserialize, Serialize};

use crate::content::Content;
use crate::lists::ListEntry;
use crate::lists::{ListId, ProblemFilter};
use crate::model::{Approach, Attempt, CompanySlugs, Difficulty, Grade, Problem, ProblemView};
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
    /// The problem, with its full company map.
    pub problem: ProblemView<'a>,
    /// Its worked approach, if one was written.
    pub approach: Option<&'a Approach>,
    /// Its Leitner state; `None` when never attempted.
    pub state: Option<CardState>,
    /// Your own answer, or `None` when you have not written one.
    pub note: Option<String>,
}

/// The next card to study in a list.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct StudyDeck<'a> {
    /// The pinned card, else the first in the queue; `None` when the set is empty.
    pub card: Option<StudyCard<'a>>,
    /// Cards left in the chosen set, including this one.
    pub remaining: usize,
    /// Every topic, most common first, for the guess picker.
    pub topics: &'a [String],
}

/// One row of the problem table: a problem of the chosen list with its progress. Topics
/// stay off so browsing does not spoil guesses.
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
    /// Whether it needs LeetCode Premium.
    pub premium: bool,
    /// Rank in the chosen list.
    pub rank: u32,
    /// Frequency in the chosen list.
    pub frequency: f32,
    /// Slugs of every company that asked it, in picker order.
    pub companies: CompanySlugs<'a>,
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
    /// With a search: the statement excerpt of a statement-only hit.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub snippet: Option<String>,
}

/// Raw query-string values of the deck endpoint.
#[derive(Debug, Clone, Copy, Default)]
pub struct DeckParams<'a> {
    /// Study set.
    pub set: Option<&'a str>,
    /// Company slug or "any".
    pub company: Option<&'a str>,
    /// Period.
    pub period: Option<&'a str>,
    /// Topic tag.
    pub topic: Option<&'a str>,
    /// Difficulty.
    pub difficulty: Option<&'a str>,
    /// Pinned problem.
    pub slug: Option<&'a str>,
}

/// Query of the deck endpoint: a list, a filter over it and an optional pinned problem.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeckQuery {
    /// Which list.
    pub list: ListId,
    /// Which cards of it.
    pub filter: QueueFilter,
    /// Show this problem instead of the next one in the queue.
    pub slug: Option<String>,
}

impl DeckQuery {
    /// Builds a query leniently: an unknown set falls back to "smart", an unknown company to
    /// the default one, an unknown period to "6m", and an unknown topic or difficulty or
    /// empty strings to no filter.
    #[must_use]
    pub fn parse(content: &Content, params: &DeckParams<'_>) -> Self {
        Self {
            list: content.list_id(params.company, params.period),
            filter: QueueFilter {
                set: params.set.and_then(|s| s.parse().ok()).unwrap_or_default(),
                problems: content.problem_filter(params.topic, params.difficulty),
            },
            slug: params.slug.filter(|s| !s.is_empty()).map(str::to_owned),
        }
    }
}

/// Raw query-string values of the problem table endpoint.
#[derive(Debug, Clone, Copy, Default)]
pub struct ProblemParams<'a> {
    /// Company slug or "any".
    pub company: Option<&'a str>,
    /// Period.
    pub period: Option<&'a str>,
    /// Topic tag.
    pub topic: Option<&'a str>,
    /// Difficulty.
    pub difficulty: Option<&'a str>,
    /// Free-text search.
    pub q: Option<&'a str>,
}

/// Query of the problem table: a list, a filter over it and an optional search.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProblemQuery<'a> {
    /// Which list.
    pub list: ListId,
    /// Which problems of it.
    pub filter: ProblemFilter,
    /// Only problems matching this search, best match first; `None` keeps list order.
    pub q: Option<&'a str>,
}

impl<'a> ProblemQuery<'a> {
    /// Builds a query leniently, like [`DeckQuery::parse`]; a blank search means none.
    #[must_use]
    pub fn parse(content: &Content, params: &ProblemParams<'a>) -> Self {
        Self {
            list: content.list_id(params.company, params.period),
            filter: content.problem_filter(params.topic, params.difficulty),
            q: params.q.filter(|q| !q.trim().is_empty()),
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
        problem: content.view(problem),
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

/// The pinned problem when it exists, else the next card of the list's set. `note_for`
/// loads the learner's answer for the chosen slug, and is called only when there is a card.
pub fn deck<'a>(
    content: &'a Content,
    states: &CardStates,
    query: &DeckQuery,
    now: i64,
    note_for: impl FnOnce(&str) -> Option<String>,
) -> StudyDeck<'a> {
    let (head, remaining) = queue_head(
        content.list_problems(query.list),
        states,
        &query.filter,
        now,
    );
    let pinned = query.slug.as_deref().and_then(|slug| content.problem(slug));
    StudyDeck {
        card: pinned
            .or(head)
            .map(|problem| card_for(content, problem, states, note_for(&problem.slug))),
        remaining,
        topics: &content.topics,
    }
}

fn row<'a>(
    content: &'a Content,
    entry: &ListEntry,
    states: &CardStates,
    now: i64,
    snippet: Option<String>,
) -> ProblemRow<'a> {
    let p = content.problem_at(entry);
    let state = states.get(&p.slug);
    ProblemRow {
        id: p.id,
        slug: &p.slug,
        title: &p.title,
        difficulty: p.difficulty,
        premium: p.premium,
        rank: entry.rank,
        frequency: entry.frequency,
        companies: p.company_slugs(&content.companies),
        status: card_status(state, now),
        list: state.and_then(|s| s.list),
        reviews: state.map_or(0, |s| s.reviews),
        last_score: state.and_then(|s| s.last_score),
        last_at: state.map(|s| s.last_at),
        due: state.map(|s| s.due),
        snippet,
    }
}

/// The problems of one list that pass the filter, with their progress: in list order, or
/// best match first with a search. Without a search this is one pass over the list.
#[must_use]
pub fn problem_rows<'a>(
    content: &'a Content,
    query: &ProblemQuery<'_>,
    states: &CardStates,
    now: i64,
) -> Vec<ProblemRow<'a>> {
    let list = content.list(query.list);
    let Some(q) = query.q else {
        return list
            .iter()
            .filter(|entry| query.filter.matches(content.problem_at(entry)))
            .map(|entry| row(content, entry, states, now, None))
            .collect();
    };
    // Where each problem sits in the list, so the search scores only the list's problems.
    let mut position = vec![u32::MAX; content.problems.len()];
    for (i, entry) in (0_u32..).zip(list) {
        position[entry.problem as usize] = i;
    }
    let entry_of = |problem: u32| list.get(position[problem as usize] as usize);
    content
        .search_index
        .matches(q, |problem| {
            entry_of(problem).is_some_and(|e| query.filter.matches(content.problem_at(e)))
        })
        .into_iter()
        .filter_map(|hit| {
            let entry = entry_of(hit.problem)?;
            Some(row(content, entry, states, now, hit.snippet))
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
    use crate::model::fixtures::{
        GOOGLE, META, T0, asked, attempt, classic, companies, problem, with,
    };
    use crate::model::{CompanyFilter, Period};
    use crate::scheduler::{StudySet, card_states};

    /// p1500 (Google rank 1), p2 (Google rank 2, Meta all-time), p3 (no company).
    fn content() -> Content {
        let google = with(classic(1500), GOOGLE, Period::Months6, asked(1, 50.0));
        let p2 = with(problem(2), META, Period::All, asked(4, 30.0));
        Content::new(companies(), vec![google, p2, classic(3)], HashMap::new())
    }

    fn params<'a>(company: Option<&'a str>, period: Option<&'a str>) -> DeckParams<'a> {
        DeckParams {
            company,
            period,
            ..DeckParams::default()
        }
    }

    #[test]
    fn parses_deck_queries_leniently() {
        let content = content();
        let q = DeckQuery::parse(
            &content,
            &DeckParams {
                set: Some("bogus"),
                period: Some("1y"),
                topic: Some(""),
                difficulty: Some("Hard"),
                ..DeckParams::default()
            },
        );
        assert_eq!(q.filter.set, StudySet::Smart);
        assert_eq!(q.list.period, Period::Months6);
        assert_eq!(q.list.company, CompanyFilter::Company(GOOGLE));
        assert_eq!(
            (
                q.filter.problems.topic,
                q.filter.problems.difficulty,
                q.slug
            ),
            (None, Some(Difficulty::Hard), None)
        );
        let q = DeckQuery::parse(
            &content,
            &DeckParams {
                set: Some("due"),
                company: Some("meta"),
                period: Some("lc1000"),
                slug: Some("p2"),
                ..DeckParams::default()
            },
        );
        assert_eq!(
            (q.filter.set, q.list.period),
            (StudySet::Due, Period::Lc1000)
        );
        assert_eq!(q.list.company, CompanyFilter::Company(META));
        assert_eq!(q.slug.as_deref(), Some("p2"));
    }

    #[test]
    fn deals_the_next_card_of_the_list_or_the_pinned_one() {
        let content = content();
        let states = CardStates::new();
        let mut asked_for = Vec::new();
        let six = DeckQuery::parse(&content, &DeckParams::default());
        let deck6 = deck(&content, &states, &six, T0, |slug| {
            asked_for.push(slug.to_owned());
            Some("my note".to_owned())
        });
        assert_eq!(deck6.remaining, 2);
        let card = deck6.card.expect("a card");
        assert_eq!(
            (card.problem.slug, card.note.as_deref()),
            ("p1500", Some("my note"))
        );
        assert_eq!(asked_for, ["p1500"]);

        let meta = DeckQuery::parse(&content, &params(Some("meta"), Some("all")));
        let deck_meta = deck(&content, &states, &meta, T0, |_| None);
        assert_eq!(
            (deck_meta.remaining, deck_meta.card.map(|c| c.problem.id)),
            (1, Some(2))
        );

        let lc = DeckQuery::parse(&content, &params(None, Some("lc1000")));
        let deck_lc = deck(&content, &states, &lc, T0, |_| None);
        assert_eq!(
            (deck_lc.remaining, deck_lc.card.map(|c| c.problem.id)),
            (2, Some(2))
        );

        let mut pinned = DeckQuery::parse(&content, &params(None, Some("30d")));
        pinned.slug = Some("p3".into());
        let deck_pinned = deck(&content, &states, &pinned, T0, |_| None);
        assert_eq!(
            (
                deck_pinned.remaining,
                deck_pinned.card.map(|c| c.problem.id)
            ),
            (0, Some(3))
        );

        // Seen cards come first: a due review beats the list's first new card.
        let states = card_states(&[attempt("p2", Grade::Again, T0)]);
        let due = deck(&content, &states, &six, T0 + crate::scheduler::DAY, |_| {
            None
        });
        assert_eq!(due.card.map(|c| c.problem.id), Some(2));
    }

    fn rows<'a>(
        content: &'a Content,
        params: &ProblemParams<'_>,
        states: &CardStates,
        now: i64,
    ) -> Vec<ProblemRow<'a>> {
        problem_rows(content, &ProblemQuery::parse(content, params), states, now)
    }

    #[test]
    fn builds_rows_for_one_list_with_progress() {
        let content = content();
        let states = card_states(&[attempt("p2", Grade::Again, T0)]);
        let rows = rows(&content, &ProblemParams::default(), &states, T0 + 1);
        let json: serde_json::Value =
            serde_json::from_str(&serde_json::to_string(&rows).expect("serialize")).expect("parse");
        assert_eq!(json.as_array().map(Vec::len), Some(2));
        assert_eq!(
            json[1],
            json!({
                "id": 2, "slug": "p2", "title": "Problem 2", "difficulty": "Medium",
                "premium": false, "rank": 2, "frequency": 10.0, "companies": ["google", "meta"],
                "status": "later", "list": "again", "reviews": 1, "lastScore": 1.0,
                "lastAt": T0, "due": T0 + 600_000,
            })
        );
        let lc = super::problem_rows(
            &content,
            &ProblemQuery {
                list: content.list_id(Some("any"), Some("lc1000")),
                filter: ProblemFilter::default(),
                q: None,
            },
            &states,
            T0,
        );
        let lc: Vec<_> = lc.iter().map(|r| (r.id, r.rank, r.frequency)).collect();
        assert_eq!(lc, [(2, 2, 30.0), (3, 3, 0.0)]);
    }

    /// p1 Easy [Graph], p2 Hard [Graph, Array], p3 Hard [Array]: all Google 6 months.
    fn tagged() -> Content {
        let mut p1 = problem(1);
        p1.difficulty = Difficulty::Easy;
        p1.topics = vec!["Graph".into()];
        let mut p2 = problem(2);
        p2.difficulty = Difficulty::Hard;
        p2.topics = vec!["Graph".into(), "Array".into()];
        let mut p3 = problem(3);
        p3.difficulty = Difficulty::Hard;
        Content::new(companies(), vec![p1, p2, p3], HashMap::new())
    }

    #[test]
    fn filters_rows_by_topic_and_difficulty_in_list_order() {
        let content = tagged();
        let states = CardStates::new();
        let ids = |topic, difficulty| {
            let params = ProblemParams {
                topic,
                difficulty,
                ..ProblemParams::default()
            };
            rows(&content, &params, &states, T0)
                .iter()
                .map(|r| r.id)
                .collect::<Vec<_>>()
        };
        assert_eq!(ids(None, None), [1, 2, 3]);
        assert_eq!(ids(Some("Graph"), None), [1, 2]);
        assert_eq!(ids(None, Some("Hard")), [2, 3]);
        assert_eq!(ids(Some("Graph"), Some("Hard")), [2]);
        assert_eq!(ids(Some("Array"), Some("Easy")), Vec::<u32>::new());
        // Unknown values filter nothing, like an unknown company or period.
        assert_eq!(ids(Some("Nope"), Some("Impossible")), [1, 2, 3]);
        assert_eq!(ids(Some(""), Some("")), [1, 2, 3]);
    }

    #[test]
    fn deals_only_cards_of_the_topic_and_difficulty() {
        let content = tagged();
        let states = CardStates::new();
        let deal = |topic, difficulty| {
            let query = DeckQuery::parse(
                &content,
                &DeckParams {
                    topic,
                    difficulty,
                    ..DeckParams::default()
                },
            );
            let deck = deck(&content, &states, &query, T0, |_| None);
            (deck.card.map(|c| c.problem.id), deck.remaining)
        };
        assert_eq!(deal(None, None), (Some(1), 3));
        assert_eq!(deal(Some("Graph"), Some("Hard")), (Some(2), 1));
        assert_eq!(deal(None, Some("Hard")), (Some(2), 2));
        assert_eq!(deal(Some("Array"), Some("Easy")), (None, 0));
    }

    #[test]
    fn searches_within_the_filtered_list_best_match_first() {
        let content = &*crate::content::testdata::CONTENT;
        let states = CardStates::new();
        let search = |q, topic, difficulty| {
            let params = ProblemParams {
                topic,
                difficulty,
                q: Some(q),
                ..ProblemParams::default()
            };
            rows(content, &params, &states, T0)
        };
        let all = search("tree", None, None);
        assert_ne!(all.len(), 0);
        let google: Vec<_> = rows(content, &ProblemParams::default(), &states, T0)
            .into_iter()
            .map(|r| r.slug)
            .collect();
        assert!(all.iter().all(|r| google.contains(&r.slug)));
        let hard = search("tree", Some("Depth-First Search"), Some("Hard"));
        assert!(!hard.is_empty() && hard.len() < all.len());
        for row in &hard {
            let p = content.problem(row.slug).expect("known");
            assert!(p.difficulty == Difficulty::Hard && p.has_topic("Depth-First Search"));
        }
        // Same order as the unfiltered search: filtering never reorders.
        let order: Vec<_> = all
            .iter()
            .map(|r| r.slug)
            .filter(|s| hard.iter().any(|h| h.slug == *s))
            .collect();
        assert_eq!(order, hard.iter().map(|r| r.slug).collect::<Vec<_>>());
        assert_eq!(search("two sum", None, None)[0].slug, "two-sum");
        // A blank search is no search: list order.
        assert_eq!(search("  ", None, None).len(), google.len());
        // Statement hits carry a snippet; the rest leave it out of the JSON.
        let statement = search("prerequisites", None, None);
        assert!(statement.iter().any(|r| r.snippet.is_some()));
        let json = serde_json::to_string(&search("two sum", None, None)[0]).expect("serialize");
        assert!(!json.contains("snippet"), "{json}");
    }

    #[test]
    fn serializes_cards_with_the_company_map() {
        let content = content();
        let states = card_states(&[attempt("p2", Grade::Less, T0)]);
        let card = card(&content, &states, "p2", None).expect("known");
        let json: serde_json::Value =
            serde_json::from_str(&serde_json::to_string(&card).expect("serialize")).expect("parse");
        assert_eq!(json["state"]["box"], 2);
        assert_eq!(json["state"]["lastGrade"], "less");
        assert_eq!(json["approach"], serde_json::Value::Null);
        assert_eq!(
            json["problem"]["companies"],
            json!({"google": {"6m": {"rank": 2, "frequency": 10.0}},
                   "meta": {"all": {"rank": 4, "frequency": 30.0}}})
        );
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
