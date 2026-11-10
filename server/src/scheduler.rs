//! Leitner scheduling: card state replayed from the attempt log, study sets and queue order.

use std::cmp::Ordering;
use std::collections::HashMap;

use serde::{Deserialize, Serialize};

use crate::lists::ProblemFilter;
use crate::model::{Attempt, Grade, Problem, wire_enum};

/// One minute in milliseconds.
pub const MINUTE: i64 = 60_000;
/// One hour in milliseconds.
pub const HOUR: i64 = 60 * MINUTE;
/// One day in milliseconds.
pub const DAY: i64 = 24 * HOUR;

/// Leitner boxes: a card in box `b` comes back after `INTERVALS[b]` milliseconds.
pub const INTERVALS: [i64; 7] = [
    10 * MINUTE,
    DAY,
    3 * DAY,
    7 * DAY,
    16 * DAY,
    35 * DAY,
    90 * DAY,
];
const TOP_BOX: usize = INTERVALS.len() - 1;
const SKIP_DELAY: i64 = HOUR;
/// "Visit less often" jumps two boxes and doubles the wait.
const LESS_FACTOR: i64 = 2;
/// A graded card whose last topic score is below this is in the "missed" set.
const MISSED_BELOW: f64 = 0.5;

wire_enum! {
    /// The list a card was graded into.
    CardList: "list" { Again = "again", Less = "less" }
}

wire_enum! {
    /// Where a card stands now.
    CardStatus: "status" { New = "new", Due = "due", Later = "later" }
}

wire_enum! {
    /// Named subsets of the deck the learner can study.
    #[derive(Default)]
    StudySet: "set" {
        #[default]
        Smart = "smart",
        Due = "due",
        New = "new",
        Again = "again",
        Less = "less",
        Missed = "missed",
        Skipped = "skipped",
        All = "all",
    }
}

impl StudySet {
    /// Label shown in the UI.
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Smart => "Due and new",
            Self::Due => "Due for review",
            Self::New => "Not seen yet",
            Self::Again => "Visit again",
            Self::Less => "Visit less often",
            Self::Missed => "Missed topics",
            Self::Skipped => "Skipped",
            Self::All => "All problems",
        }
    }
}

/// The current Leitner state of one card.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct CardState {
    /// Leitner box, an index into [`INTERVALS`].
    #[serde(rename = "box")]
    pub box_: usize,
    /// When the card is next due, Unix milliseconds.
    pub due: i64,
    /// The list the last grade put it on.
    pub list: Option<CardList>,
    /// Graded (non-skip) attempts so far.
    pub reviews: u32,
    /// Time of the last attempt, skips included.
    pub last_at: i64,
    /// Topic score of the last graded attempt.
    pub last_score: Option<f64>,
    /// Grade of the last attempt, skips included.
    pub last_grade: Grade,
}

impl CardState {
    /// The state of a card never attempted.
    pub const UNSEEN: Self = Self {
        box_: 0,
        due: 0,
        list: None,
        reviews: 0,
        last_at: 0,
        last_score: None,
        last_grade: Grade::Skip,
    };
}

/// Card state per problem slug.
pub type CardStates = HashMap<String, CardState>;

/// The state after one more attempt. A skip only defers the card: it keeps its box, list and
/// score, and never brings the card back sooner.
#[must_use]
pub fn apply_attempt(state: Option<&CardState>, attempt: &Attempt) -> CardState {
    let prev = state.copied().unwrap_or(CardState::UNSEEN);
    let at = attempt.at;
    let (box_, list, factor) = match attempt.grade {
        Grade::Skip => {
            return CardState {
                due: prev.due.max(at + SKIP_DELAY),
                last_at: at,
                last_grade: Grade::Skip,
                ..prev
            };
        }
        Grade::Again => (0, Some(CardList::Again), 1),
        Grade::Good => ((prev.box_ + 1).min(TOP_BOX), None, 1),
        Grade::Less => (
            (prev.box_ + 2).min(TOP_BOX),
            Some(CardList::Less),
            LESS_FACTOR,
        ),
    };
    CardState {
        box_,
        due: at + INTERVALS[box_] * factor,
        list,
        reviews: prev.reviews + 1,
        last_at: at,
        last_score: attempt.score,
        last_grade: attempt.grade,
    }
}

/// Folds one attempt into `states` in place, so a cache can stay current without a replay.
pub fn record_attempt(states: &mut CardStates, attempt: &Attempt) {
    if let Some(state) = states.get_mut(&attempt.slug) {
        *state = apply_attempt(Some(state), attempt);
    } else {
        states.insert(attempt.slug.clone(), apply_attempt(None, attempt));
    }
}

/// Replays the attempt log (oldest first) into the current state of every touched card.
#[must_use]
pub fn card_states(attempts: &[Attempt]) -> CardStates {
    let mut states = CardStates::new();
    for attempt in attempts {
        record_attempt(&mut states, attempt);
    }
    states
}

/// Where a card stands at `now`. A skipped card that was never graded goes back to "new"
/// once its skip delay ends.
#[must_use]
pub fn card_status(state: Option<&CardState>, now: i64) -> CardStatus {
    match state {
        Some(s) if s.due > now => CardStatus::Later,
        Some(s) if s.reviews > 0 => CardStatus::Due,
        _ => CardStatus::New,
    }
}

/// Whether a card belongs to a study set at `now`.
#[must_use]
pub fn in_set(set: StudySet, state: Option<&CardState>, now: i64) -> bool {
    let list = state.and_then(|s| s.list);
    match set {
        StudySet::Smart => card_status(state, now) != CardStatus::Later,
        StudySet::Due => card_status(state, now) == CardStatus::Due,
        StudySet::New => card_status(state, now) == CardStatus::New,
        StudySet::Again => list == Some(CardList::Again),
        StudySet::Less => list == Some(CardList::Less),
        StudySet::Missed => state
            .and_then(|s| s.last_score)
            .is_some_and(|score| score < MISSED_BELOW),
        StudySet::Skipped => state.is_some_and(|s| s.last_grade == Grade::Skip),
        StudySet::All => true,
    }
}

/// Which cards of a list to study.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct QueueFilter {
    /// The study set.
    pub set: StudySet,
    /// Only problems with this topic and difficulty.
    pub problems: ProblemFilter,
}

/// Queue order key: due reviews (visit-again first, then oldest due), then new problems in
/// list order, then cards not yet due (soonest first).
type Key = (u8, u8, i64);

fn priority(position: usize, state: Option<&CardState>, now: i64) -> Key {
    match (card_status(state, now), state) {
        (CardStatus::Due, Some(s)) => (0, u8::from(s.list != Some(CardList::Again)), s.due),
        (CardStatus::Later, Some(s)) => (2, 0, s.due),
        _ => (1, 0, i64::try_from(position).unwrap_or(i64::MAX)),
    }
}

/// Every problem of `list` passing the filter, with its queue key, in list order.
fn ranked<'p>(
    list: impl IntoIterator<Item = &'p Problem>,
    states: &CardStates,
    filter: &QueueFilter,
    now: i64,
) -> impl Iterator<Item = (Key, &'p Problem)> {
    list.into_iter().enumerate().filter_map(move |(i, p)| {
        // The bit test first, so filtered-out problems never hash their slug.
        if !filter.problems.matches(p) {
            return None;
        }
        let state = states.get(&p.slug);
        in_set(filter.set, state, now).then(|| (priority(i, state, now), p))
    })
}

/// The problems of a study list (given in new-card order) that are in the set, in the order
/// they will be shown.
#[must_use]
pub fn queue<'p>(
    list: impl IntoIterator<Item = &'p Problem>,
    states: &CardStates,
    filter: &QueueFilter,
    now: i64,
) -> Vec<&'p Problem> {
    let mut keyed: Vec<_> = ranked(list, states, filter, now).collect();
    // Stable, so ties keep list order.
    keyed.sort_by_key(|&(key, _)| key);
    keyed.into_iter().map(|(_, p)| p).collect()
}

/// The first card of [`queue`] and the queue's length, in one pass without sorting or
/// allocating.
#[must_use]
pub fn queue_head<'p>(
    list: impl IntoIterator<Item = &'p Problem>,
    states: &CardStates,
    filter: &QueueFilter,
    now: i64,
) -> (Option<&'p Problem>, usize) {
    let mut head: Option<(Key, &'p Problem)> = None;
    let mut count = 0;
    for (key, problem) in ranked(list, states, filter, now) {
        count += 1;
        // Strictly smaller only, so ties keep the earliest problem like the stable sort.
        if head.is_none_or(|(best, _)| key.cmp(&best) == Ordering::Less) {
            head = Some((key, problem));
        }
    }
    (head.map(|(_, p)| p), count)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::Difficulty;
    use crate::model::fixtures::{T0, attempt, attempt_scored, problem};

    fn slugs(list: &[&Problem]) -> Vec<String> {
        list.iter().map(|p| p.slug.clone()).collect()
    }

    #[test]
    fn schedules_each_grade_and_keeps_lists() {
        let states = card_states(&[
            attempt("good", Grade::Good, T0),
            attempt("again", Grade::Good, T0),
            attempt("again", Grade::Again, T0 + DAY),
            attempt("less", Grade::Less, T0),
            attempt("skip", Grade::Skip, T0),
        ]);
        let good = states["good"];
        assert_eq!(
            (good.box_, good.list, good.due),
            (1, None, T0 + INTERVALS[1])
        );
        let again = states["again"];
        assert_eq!((again.box_, again.list), (0, Some(CardList::Again)));
        let less = states["less"];
        assert_eq!(
            (less.box_, less.list, less.due),
            (2, Some(CardList::Less), T0 + 2 * INTERVALS[2])
        );
        let skip = states["skip"];
        assert_eq!((skip.reviews, skip.last_grade), (0, Grade::Skip));
        // Skipping a card that is due much later never brings it back sooner.
        let later = card_states(&[
            attempt("x", Grade::Less, T0),
            attempt("x", Grade::Skip, T0 + 1),
        ]);
        assert_eq!(later["x"].due, T0 + 2 * INTERVALS[2]);
    }

    #[test]
    fn incremental_updates_match_a_replay() {
        let log = [
            attempt("a", Grade::Good, T0),
            attempt("a", Grade::Less, T0 + DAY),
            attempt("b", Grade::Skip, T0),
            attempt("a", Grade::Skip, T0 + 2 * DAY),
        ];
        let mut states = CardStates::new();
        for a in &log {
            record_attempt(&mut states, a);
        }
        assert_eq!(states, card_states(&log));
        assert_eq!(states["a"].box_, 3);
    }

    #[test]
    fn orders_due_reviews_then_new_in_list_order() {
        let problems = [problem(1), problem(2), problem(3), problem(4)];
        let states = card_states(&[
            attempt("p3", Grade::Good, T0),
            attempt("p4", Grade::Again, T0),
            attempt("p2", Grade::Skip, T0),
        ]);
        let filter = QueueFilter::default();
        let at = |t| slugs(&queue(&problems, &states, &filter, t));
        assert_eq!(at(T0 + 1), ["p1"]);
        assert_eq!(at(T0 + 2 * DAY), ["p4", "p3", "p1", "p2"]);
        let (head, count) = queue_head(&problems, &states, &filter, T0 + 2 * DAY);
        assert_eq!((head.map(|p| p.slug.as_str()), count), (Some("p4"), 4));
        // New cards follow the order the list gives, not the problem numbers.
        let reversed: Vec<&Problem> = problems.iter().rev().collect();
        let order = queue(reversed.iter().copied(), &CardStates::new(), &filter, T0);
        assert_eq!(slugs(&order), ["p4", "p3", "p2", "p1"]);
    }

    #[test]
    fn filters_sets_by_list_topic_difficulty_and_missed_topics() {
        const GRAPH: u8 = 7;
        let mut p1 = problem(1);
        p1.topic_set.insert(GRAPH);
        p1.difficulty = Difficulty::Hard;
        let mut p2 = problem(2);
        p2.topic_set.insert(GRAPH);
        let problems = [p1, p2, problem(3)];
        let states = card_states(&[
            attempt_scored("p1", Grade::Less, T0, Some(0.2)),
            attempt_scored("p2", Grade::Less, T0, Some(0.9)),
            attempt("p3", Grade::Less, T0),
        ]);
        let run = |filter: QueueFilter| slugs(&queue(&problems, &states, &filter, T0));
        assert_eq!(
            run(QueueFilter {
                set: StudySet::Less,
                problems: ProblemFilter {
                    topic: Some(GRAPH),
                    difficulty: Some(Difficulty::Hard),
                },
            }),
            ["p1"]
        );
        assert_eq!(
            run(QueueFilter {
                set: StudySet::Less,
                problems: ProblemFilter {
                    topic: Some(GRAPH),
                    difficulty: None,
                },
            }),
            ["p1", "p2"]
        );
        assert_eq!(
            run(QueueFilter {
                set: StudySet::Missed,
                ..QueueFilter::default()
            }),
            ["p1"]
        );
    }
}
