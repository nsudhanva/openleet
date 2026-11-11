//! Readiness for a company: how much of its most-asked problems you can solve in the judge
//! and still recall on a flashcard, weighted by how often it asks each, and the same at the
//! end of each recent day.
//!
//! For each of the company's [`MOST_ASKED`] most-asked problems `p`, with frequency `f`:
//! readiness = Σ f·(0.6·code + 0.4·card) / Σ f, where code is 1 for a clean solve in the judge,
//! 0.5 for a shaky one and 0 otherwise, and card is 1 when the card's last grade was "Got it"
//! or "Visit less often" and it is not overdue, 0.5 when it is overdue by less than its
//! interval, and 0 otherwise.

use std::collections::{BTreeSet, HashMap};

use jiff::ToSpan;
use jiff::civil::Date;
use jiff::tz::TimeZone;
use serde::Serialize;

use crate::coding::{Judged, ProblemSubmissions};
use crate::content::Content;
use crate::insights::{Learner, iso_date};
use crate::lists::ListId;
use crate::model::{Attempt, CompanyFilter, Period, Problem};
use crate::scheduler::{CardList, CardState, apply_attempt};
use crate::scorer::{civil_day, day_end};

/// How many of the most-asked problems readiness covers, at most.
pub const MOST_ASKED: usize = 100;
/// A 6-month list shorter than this is too short to judge by: the all-time list is used.
pub const MIN_RECENT: usize = 25;
/// The share of a problem's score that solving it in the judge earns.
const CODE_SHARE: f64 = 0.6;
/// The share that a current flashcard earns.
const CARD_SHARE: f64 = 0.4;
/// The trend covers at most this many days, ending today.
pub const TREND_DAYS: i64 = 90;
/// The trend waits for this many distinct days with practice.
pub const TREND_MIN_DAYS: usize = 7;

/// The problems readiness covers: the company's most-asked from its 6-month list, or from
/// its all-time list when the 6-month one has fewer than [`MIN_RECENT`] problems.
#[derive(Debug, Clone)]
pub struct ReadinessList<'a> {
    /// The list they come from: [`Period::Months6`] or [`Period::All`].
    pub period: Period,
    /// The problems with their weights, most asked first.
    pub problems: Vec<(&'a Problem, f64)>,
    /// How many problems the 6-month list has.
    pub recent: usize,
}

/// The company's (or any company's) readiness list.
#[must_use]
pub fn readiness_list(content: &Content, company: CompanyFilter) -> ReadinessList<'_> {
    let list = |period| content.list(ListId { company, period });
    let recent = list(Period::Months6).len();
    let period = if recent < MIN_RECENT {
        Period::All
    } else {
        Period::Months6
    };
    let mut entries = list(period).to_vec();
    // A stable sort keeps the list's rank order among equal frequencies.
    entries.sort_by(|a, b| b.frequency.total_cmp(&a.frequency));
    entries.truncate(MOST_ASKED);
    // Weighted by frequency; a list that gives none weighs every problem the same.
    let unweighted = entries.iter().all(|e| e.frequency <= 0.0);
    let problems = entries
        .iter()
        .map(|e| {
            let weight = if unweighted {
                1.0
            } else {
                f64::from(e.frequency.max(0.0))
            };
            (content.problem_at(e), weight)
        })
        .collect();
    ReadinessList {
        period,
        problems,
        recent,
    }
}

/// How much of its share one side of a problem earns.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Credit {
    Full,
    Half,
    Nothing,
}

impl Credit {
    /// The share earned: 1, 0.5 or 0.
    #[must_use]
    pub const fn value(self) -> f64 {
        match self {
            Self::Full => 1.0,
            Self::Half => 0.5,
            Self::Nothing => 0.0,
        }
    }
}

/// A problem's coding credit: full for a clean solve, half for a shaky one, none unsolved.
#[must_use]
pub fn code_credit(submissions: Option<&ProblemSubmissions>) -> Credit {
    match submissions {
        Some(s) if s.shaky() => Credit::Half,
        Some(s) if s.solved() => Credit::Full,
        _ => Credit::Nothing,
    }
}

/// A card's credit at `at`: full when its last grade was "Got it" or "Visit less often" and
/// it is not overdue, half when it is overdue by less than its interval, none otherwise
/// (never graded, or last graded "Visit again"). A skip only defers a card, so it changes
/// nothing here but the due time.
#[must_use]
pub fn card_credit(state: Option<&CardState>, at: i64) -> Credit {
    let Some(state) = state.filter(|s| s.reviews > 0 && s.list != Some(CardList::Again)) else {
        return Credit::Nothing;
    };
    let overdue = at - state.due;
    if overdue <= 0 {
        Credit::Full
    } else if overdue < state.interval() {
        Credit::Half
    } else {
        Credit::Nothing
    }
}

/// Readiness for one company's list.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Readiness {
    /// 0..1; `None` before any card of these problems was graded or any of them submitted.
    pub score: Option<f64>,
    /// The list the problems come from: "6m", or "all" when the 6-month list is too short.
    pub period: Period,
    /// How many problems it covers.
    pub problems: usize,
    /// How many problems the 6-month list has.
    pub recent: usize,
    /// Of the problems, solved cleanly in the judge.
    pub solved: usize,
    /// Of the problems, solved but shaky.
    pub shaky: usize,
    /// Of the problems, cards graded "Got it" or "Visit less often" and not overdue.
    pub cards: usize,
    /// Of the problems, such cards overdue by less than their interval.
    pub fading: usize,
}

/// Readiness at `at` from each problem's card state and submissions, in list order.
fn blend<'s>(
    list: &ReadinessList<'_>,
    learned: impl IntoIterator<Item = (Option<&'s CardState>, Option<&'s ProblemSubmissions>)>,
    at: i64,
) -> Readiness {
    let mut readiness = Readiness {
        score: None,
        period: list.period,
        problems: list.problems.len(),
        recent: list.recent,
        solved: 0,
        shaky: 0,
        cards: 0,
        fading: 0,
    };
    let (mut weight, mut weighted, mut touched) = (0.0, 0.0, false);
    for ((_, w), (card, submissions)) in list.problems.iter().zip(learned) {
        let code = code_credit(submissions);
        let current = card_credit(card, at);
        readiness.solved += usize::from(code == Credit::Full);
        readiness.shaky += usize::from(code == Credit::Half);
        readiness.cards += usize::from(current == Credit::Full);
        readiness.fading += usize::from(current == Credit::Half);
        touched |= submissions.is_some() || card.is_some_and(|c| c.reviews > 0);
        weight += w;
        weighted += w * (CODE_SHARE * code.value() + CARD_SHARE * current.value());
    }
    if touched && weight > 0.0 {
        readiness.score = Some(weighted / weight);
    }
    readiness
}

/// Readiness at `now`.
#[must_use]
pub fn readiness(list: &ReadinessList<'_>, learner: Learner<'_>, now: i64) -> Readiness {
    let learned = list
        .problems
        .iter()
        .map(|(p, _)| (learner.states.get(&p.slug), learner.coding.problem(&p.slug)));
    blend(list, learned, now)
}

/// Readiness at the end of one day.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct TrendPoint {
    /// The calendar day, in the server's time zone.
    #[serde(serialize_with = "iso_date")]
    pub day: Date,
    /// Readiness at the day's end (today: now), 0..1.
    pub readiness: f64,
}

/// Readiness over the recent days.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Trend {
    /// Distinct days with practice, ever.
    pub practice_days: usize,
    /// Readiness at the end of each day from the first day with practice (at most
    /// [`TREND_DAYS`] back) to today, leaving out the days before readiness had any data;
    /// empty until [`TREND_MIN_DAYS`] days with practice.
    pub points: Vec<TrendPoint>,
}

/// One problem's history, replayed day by day.
struct Replay<'a> {
    attempts: Vec<&'a Attempt>,
    judged: &'a [Judged],
    /// How many attempts and submissions are replayed so far.
    next: (usize, usize),
    card: Option<CardState>,
    code: Option<ProblemSubmissions>,
}

/// Readiness at the end of each recent day, replayed from the logs: every attempt and
/// submission up to a day's end, judged at that moment. `days` are the days with practice.
#[must_use]
pub fn trend(
    list: &ReadinessList<'_>,
    learner: Learner<'_>,
    days: &BTreeSet<Date>,
    now: i64,
    tz: &TimeZone,
) -> Trend {
    let mut trend = Trend {
        practice_days: days.len(),
        points: Vec::new(),
    };
    let Some(&first) = days.first() else {
        return trend;
    };
    if days.len() < TREND_MIN_DAYS {
        return trend;
    }
    let index: HashMap<&str, usize> = (0..)
        .zip(&list.problems)
        .map(|(i, (p, _))| (p.slug.as_str(), i))
        .collect();
    let mut replays: Vec<Replay<'_>> = list
        .problems
        .iter()
        .map(|(p, _)| Replay {
            attempts: Vec::new(),
            judged: learner.coding.judged(&p.slug),
            next: (0, 0),
            card: None,
            code: None,
        })
        .collect();
    for attempt in learner.attempts {
        if let Some(&i) = index.get(attempt.slug.as_str()) {
            replays[i].attempts.push(attempt);
        }
    }
    let today = civil_day(now, tz);
    let window = today.checked_sub((TREND_DAYS - 1).days()).unwrap_or(today);
    let mut day = first.max(window);
    while day <= today {
        let end = if day == today { now } else { day_end(day, tz) };
        for r in &mut replays {
            while let Some(attempt) = r.attempts.get(r.next.0).filter(|a| a.at <= end) {
                r.card = Some(apply_attempt(r.card.as_ref(), attempt));
                r.next.0 += 1;
            }
            while let Some(&(at, verdict)) = r.judged.get(r.next.1).filter(|j| j.0 <= end) {
                r.code
                    .get_or_insert_default()
                    .record(verdict, at, learner.coding.tz());
                r.next.1 += 1;
            }
        }
        let learned = replays.iter().map(|r| (r.card.as_ref(), r.code.as_ref()));
        if let Some(readiness) = blend(list, learned, end).score {
            trend.points.push(TrendPoint { day, readiness });
        }
        let Ok(next) = day.tomorrow() else { break };
        day = next;
    }
    trend
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use openleet_proto::Verdict;

    use super::*;
    use crate::coding::CodingLog;
    use crate::insights::practice_days;
    use crate::model::fixtures::{GOOGLE, META, T0, asked, attempt, classic, companies, with};
    use crate::model::{Attempt, Grade};
    use crate::scheduler::{CardStates, DAY, HOUR, INTERVALS, card_states};

    const G: CompanyFilter = CompanyFilter::Company(GOOGLE);
    const UTC: TimeZone = TimeZone::UTC;

    /// `recent` problems in Google's 6-month list and `all` in its all-time list (p1 first,
    /// p1 asked most, frequency 100, the rest 10); Meta asks only p1, in 6 months.
    fn content(recent: u16, all: u16) -> Content {
        let problems = (1..=recent.max(all))
            .map(|rank| {
                let frequency = if rank == 1 { 100.0 } else { 10.0 };
                let mut p = classic(u32::from(rank));
                if rank <= recent {
                    p = with(p, GOOGLE, Period::Months6, asked(rank, frequency));
                }
                if rank <= all {
                    p = with(p, GOOGLE, Period::All, asked(rank, frequency));
                }
                if rank == 1 {
                    p = with(p, META, Period::Months6, asked(1, 50.0));
                }
                p
            })
            .collect();
        Content::new(companies(), problems, HashMap::new())
    }

    struct Logs {
        attempts: Vec<Attempt>,
        states: CardStates,
        coding: CodingLog,
    }

    fn logs(attempts: &[Attempt], submissions: &[(&str, i64, Verdict)]) -> Logs {
        let mut coding = CodingLog::new(UTC);
        for &(slug, at, verdict) in submissions {
            coding.record(slug, at, verdict);
        }
        Logs {
            attempts: attempts.to_vec(),
            states: card_states(attempts),
            coding,
        }
    }

    impl Logs {
        fn learner(&self) -> Learner<'_> {
            Learner {
                attempts: &self.attempts,
                states: &self.states,
                coding: &self.coding,
            }
        }
    }

    fn close(a: Option<f64>, b: f64) -> bool {
        a.is_some_and(|a| (a - b).abs() < 1e-9)
    }

    #[test]
    fn covers_the_hundred_most_asked_of_the_six_month_list() {
        let content = content(120, 120);
        let list = readiness_list(&content, G);
        assert_eq!(
            (list.period, list.problems.len(), list.recent),
            (Period::Months6, 100, 120)
        );
        // Most asked first, then in rank order.
        assert_eq!(list.problems[0].0.slug, "p1");
        assert_eq!(list.problems[1].0.slug, "p2");
        assert_eq!(list.problems[99].0.slug, "p100");
        assert!((list.problems[0].1 - 100.0).abs() < 1e-9);
    }

    #[test]
    fn a_short_six_month_list_falls_back_to_all_time() {
        // 25 problems in 6 months is enough; 24 is not.
        let enough = content(25, 40);
        let list = readiness_list(&enough, G);
        assert_eq!((list.period, list.problems.len()), (Period::Months6, 25));
        let short = content(24, 40);
        let list = readiness_list(&short, G);
        assert_eq!(
            (list.period, list.problems.len(), list.recent),
            (Period::All, 40, 24)
        );
        // Meta asks one problem in 6 months and none at any time: nothing to cover.
        let meta = readiness_list(&short, CompanyFilter::Company(META));
        assert_eq!(
            (meta.period, meta.problems.len(), meta.recent),
            (Period::All, 0, 1)
        );
        let logs = logs(&[attempt("p1", Grade::Good, T0)], &[]);
        let readiness = readiness(&meta, logs.learner(), T0);
        assert_eq!((readiness.score, readiness.problems), (None, 0));
    }

    #[test]
    fn credits_a_card_by_its_last_grade_and_how_overdue_it_is() {
        use Credit::{Full, Half, Nothing};
        let state = |grades: &[Grade]| {
            let log: Vec<_> = (0_i64..)
                .zip(grades)
                .map(|(i, &g)| attempt("p1", g, T0 + i))
                .collect();
            card_states(&log).remove("p1")
        };
        assert_eq!(card_credit(None, T0), Nothing);
        let good = state(&[Grade::Good]).expect("graded");
        // "Got it" from box 0 waits a day.
        assert_eq!(good.interval(), INTERVALS[1]);
        let at = |offset| card_credit(Some(&good), good.due + offset);
        assert_eq!(
            [at(0), at(1), at(good.interval() - 1), at(good.interval())],
            [Full, Half, Half, Nothing]
        );
        // "Visit less often" counts like "Got it", over its own (longer) interval.
        let less = state(&[Grade::Less]).expect("graded");
        assert_eq!(less.interval(), 2 * INTERVALS[2]);
        assert_eq!(card_credit(Some(&less), less.due), Full);
        assert_eq!(
            card_credit(Some(&less), less.due + less.interval() - 1),
            Half
        );
        // "Visit again" and a card only skipped earn nothing; a skip after "Got it" changes
        // nothing but when it is due.
        assert_eq!(card_credit(state(&[Grade::Again]).as_ref(), T0), Nothing);
        assert_eq!(card_credit(state(&[Grade::Skip]).as_ref(), T0), Nothing);
        let skipped = state(&[Grade::Good, Grade::Skip]).expect("graded");
        assert_eq!(card_credit(Some(&skipped), T0 + HOUR), Full);
    }

    #[test]
    fn credits_code_clean_shaky_or_unsolved() {
        use Verdict::*;
        let log = logs(
            &[],
            &[
                ("p1", T0, Accepted),
                ("p2", T0, TimeLimitExceeded),
                ("p2", T0 + 1, Accepted),
                ("p3", T0, WrongAnswer),
            ],
        )
        .coding;
        let credit = |slug| code_credit(log.problem(slug));
        assert_eq!(
            [credit("p1"), credit("p2"), credit("p3"), credit("p4")],
            [Credit::Full, Credit::Half, Credit::Nothing, Credit::Nothing]
        );
    }

    #[test]
    fn blends_code_and_cards_weighted_by_frequency() {
        use Verdict::*;
        let thirty = content(30, 30);
        let list = readiness_list(&thirty, G);
        // No grade and no submission on the list: nothing to score yet, not 0%.
        let elsewhere = logs(
            &[attempt("p999", Grade::Good, T0)],
            &[("p999", T0, Accepted)],
        );
        let empty = readiness(&list, elsewhere.learner(), T0);
        assert_eq!(empty.score, None);
        assert_eq!((empty.problems, empty.solved, empty.cards), (30, 0, 0));
        // p1 (100): solved cleanly and its card current. p2 (10): a shaky solve. p3 (10): a
        // card graded "Visit again". The other 27 weigh 10 each and score nothing.
        let learned = logs(
            &[
                attempt("p1", Grade::Good, T0),
                attempt("p3", Grade::Again, T0),
            ],
            &[
                ("p1", T0, Accepted),
                ("p2", T0, TimeLimitExceeded),
                ("p2", T0 + 1, Accepted),
            ],
        );
        let now = readiness(&list, learned.learner(), T0 + HOUR);
        let total = 100.0 + 29.0 * 10.0;
        assert!(close(now.score, (100.0 + 10.0 * 0.6 * 0.5) / total));
        assert_eq!((now.solved, now.shaky, now.cards, now.fading), (1, 1, 1, 0));
        // A day and a half later p1's card is overdue by half its interval: half its share.
        let later = readiness(&list, learned.learner(), T0 + DAY + DAY / 2);
        assert!(close(later.score, (100.0 * (0.6 + 0.2) + 3.0) / total));
        assert_eq!((later.cards, later.fading), (0, 1));
        // Two days past due it is worth nothing on the card side.
        let gone = readiness(&list, learned.learner(), T0 + 3 * DAY);
        assert!(close(gone.score, (100.0 * 0.6 + 3.0) / total));
        // A list with only one problem: all of it, or nothing.
        let tiny = content(1, 1);
        let one = readiness(&readiness_list(&tiny, G), learned.learner(), T0 + HOUR);
        assert_eq!((one.period, one.problems), (Period::All, 1));
        assert!(close(one.score, 1.0));
    }

    #[test]
    fn the_trend_waits_for_seven_days_of_practice() {
        let content = content(30, 30);
        let list = readiness_list(&content, G);
        let six: Vec<_> = (0..6)
            .map(|d| attempt("p1", Grade::Good, T0 + d * DAY))
            .collect();
        let logs = logs(&six, &[]);
        let days = practice_days(&logs.attempts, &logs.coding, &UTC);
        let trend = trend(&list, logs.learner(), &days, T0 + 6 * DAY, &UTC);
        assert_eq!(trend.practice_days, 6);
        assert!(trend.points.is_empty());
    }

    #[test]
    fn the_trend_replays_the_logs_to_each_day_end() {
        use Verdict::*;
        let content = content(30, 30);
        let list = readiness_list(&content, G);
        // Day 0 practices another list only; p1's card is graded on days 1 and 2 (then due
        // on day 5), and p1 solved on day 4, after a wrong answer on day 3. Practice also on
        // days 5, 7 and 9 (skipping 6 and 8), elsewhere.
        let attempts = [
            attempt("p999", Grade::Good, T0),
            attempt("p1", Grade::Good, T0 + DAY),
            attempt("p1", Grade::Good, T0 + 2 * DAY),
            attempt("p999", Grade::Good, T0 + 5 * DAY),
            attempt("p999", Grade::Good, T0 + 7 * DAY),
        ];
        let submissions = [
            ("p1", T0 + 3 * DAY, WrongAnswer),
            ("p1", T0 + 4 * DAY, Accepted),
            ("p999", T0 + 9 * DAY, Accepted),
        ];
        let logs = logs(&attempts, &submissions);
        let days = practice_days(&logs.attempts, &logs.coding, &UTC);
        assert_eq!(days.len(), 8);
        let now = T0 + 9 * DAY + HOUR;
        let trend = trend(&list, logs.learner(), &days, now, &UTC);
        let total = 100.0 + 29.0 * 10.0;
        let points: Vec<_> = trend
            .points
            .iter()
            .map(|p| (p.day.to_string(), (p.readiness * total).round()))
            .collect();
        // Day 0 has no data for this list, so the line starts on day 1; every day after has
        // a point, practice or not. p1's card (box 2 after day 2, so due at the start of day
        // 5 with a 3-day interval) is current through day 4, half its share on days 5 to 7,
        // then nothing; its code counts from day 4.
        assert_eq!(
            points,
            [
                ("2026-01-02".to_owned(), 40.0),
                ("2026-01-03".to_owned(), 40.0),
                ("2026-01-04".to_owned(), 40.0),
                ("2026-01-05".to_owned(), 100.0),
                ("2026-01-06".to_owned(), 80.0),
                ("2026-01-07".to_owned(), 80.0),
                ("2026-01-08".to_owned(), 80.0),
                ("2026-01-09".to_owned(), 60.0),
                ("2026-01-10".to_owned(), 60.0),
            ]
        );
        // Today's point is readiness now.
        let current = readiness(&list, logs.learner(), now);
        assert!(close(
            current.score,
            trend.points.last().expect("today").readiness
        ));
        let json = serde_json::to_value(&trend).expect("json");
        assert_eq!(json["practiceDays"], 8);
        assert_eq!(json["points"][0]["day"], "2026-01-02");
    }

    #[test]
    fn the_trend_covers_at_most_ninety_days() {
        let content = content(30, 30);
        let list = readiness_list(&content, G);
        let attempts: Vec<_> = (0..200)
            .map(|d| attempt("p1", Grade::Less, T0 + d * DAY))
            .collect();
        let logs = logs(&attempts, &[]);
        let days = practice_days(&logs.attempts, &logs.coding, &UTC);
        let now = T0 + 199 * DAY;
        let trend = trend(&list, logs.learner(), &days, now, &UTC);
        assert_eq!(trend.points.len(), 90);
        assert_eq!(trend.points[89].day, civil_day(now, &UTC));
    }
}
