//! Topic-guess scoring and the report.
//!
//! Readiness and its trend cover the company's most-asked problems (see [`crate::readiness`]),
//! the study counts and cards by difficulty its 6-month list. Topic accuracy, the graded
//! count, the topics you name least and the streak count every list.

use std::collections::HashSet;

use jiff::Timestamp;
use jiff::civil::Date;
use jiff::tz::TimeZone;
use serde::Serialize;

use crate::content::Content;
use crate::insights::{Learner, practice_days, streak};
use crate::lists::ListId;
use crate::model::{Attempt, CompanyFilter, Difficulty, Grade, MAX_TOPICS, Period, TopicId};
use crate::readiness::{Readiness, Trend, readiness, readiness_list, trend};
use crate::scheduler::{CardList, CardStatus, card_status};

/// How a topic guess compares with the problem's tags.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct TopicResult {
    /// Tags guessed correctly, in tag order.
    pub hits: Vec<String>,
    /// Tags not guessed, in tag order.
    pub missed: Vec<String>,
    /// Guesses that are not tags, in guess order.
    pub extra: Vec<String>,
    /// F1 of the guess against the listed topics.
    pub score: f64,
}

/// Scores a topic guess against the problem's tags with F1.
#[must_use]
pub fn score_topics(guessed: &[String], actual: &[String]) -> TopicResult {
    let truth: HashSet<&str> = actual.iter().map(String::as_str).collect();
    let guess: HashSet<&str> = guessed.iter().map(String::as_str).collect();
    let (hits, missed): (Vec<String>, Vec<String>) = actual
        .iter()
        .cloned()
        .partition(|t| guess.contains(t.as_str()));
    let extra: Vec<String> = guessed
        .iter()
        .filter(|t| !truth.contains(t.as_str()))
        .cloned()
        .collect();
    let total = guess.len() + truth.len();
    let score = if total == 0 {
        0.0
    } else {
        ratio(2 * hits.len(), total)
    };
    TopicResult {
        hits,
        missed,
        extra,
        score,
    }
}

/// Accuracy averages this many most recent graded attempts.
const RECENT_ATTEMPTS: usize = 50;
/// A topic is rated once this many graded cards carried it.
pub const MIN_TOPIC_CARDS: usize = 5;
/// Topics rated below this are listed as the ones you name least.
const WEAK_TOPIC_BELOW: f64 = 0.6;

/// `num / den` as a float; counts here are far below 2^53.
#[allow(clippy::cast_precision_loss)]
pub(crate) fn ratio(num: usize, den: usize) -> f64 {
    num as f64 / den as f64
}

/// Cards per study state, over the selected company's 6-month list.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize)]
pub struct Counts {
    /// Seen cards due now.
    pub due: usize,
    /// Cards never graded.
    pub new: usize,
    /// Cards on the visit-again list.
    pub again: usize,
    /// Cards on the visit-less-often list.
    pub less: usize,
}

/// How many cards of one difficulty were graded, over the selected company's 6-month list.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct DifficultyCoverage {
    /// The difficulty.
    pub difficulty: Difficulty,
    /// Problems graded at least once.
    pub seen: usize,
    /// Problems of this difficulty.
    pub total: usize,
}

/// How a topic fared on graded cards: named when it applied, missed when it applied, and
/// named when it did not (a false alarm).
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct TopicTally {
    /// Graded cards with the topic that named it.
    pub named: usize,
    /// Graded cards with the topic.
    pub seen: usize,
    /// Graded cards without the topic that named it.
    pub false_alarms: usize,
}

impl TopicTally {
    /// Named over named plus half the mistakes (misses and false alarms), an F1 for the
    /// topic: naming it on every card scores no better than never naming it. `None` before
    /// [`MIN_TOPIC_CARDS`] graded cards carried it.
    #[must_use]
    pub fn score(self) -> Option<f64> {
        if self.seen < MIN_TOPIC_CARDS {
            return None;
        }
        let mistakes = self.seen - self.named + self.false_alarms;
        Some(ratio(2 * self.named, 2 * self.named + mistakes))
    }
}

/// Every topic's tally over graded attempts, indexed by [`TopicId`].
pub fn topic_tallies<'a>(
    content: &Content,
    graded: impl IntoIterator<Item = &'a Attempt>,
) -> Vec<TopicTally> {
    let mut tallies = vec![TopicTally::default(); MAX_TOPICS];
    for attempt in graded {
        let Some(problem) = content.problem(&attempt.slug) else {
            continue;
        };
        let guessed: HashSet<TopicId> = attempt
            .guessed
            .iter()
            .filter_map(|g| content.topic_id(g))
            .collect();
        for id in problem.topic_set.iter() {
            let t = &mut tallies[usize::from(id)];
            t.seen += 1;
            t.named += usize::from(guessed.contains(&id));
        }
        for &id in &guessed {
            if !problem.topic_set.contains(id) {
                tallies[usize::from(id)].false_alarms += 1;
            }
        }
    }
    tallies
}

/// A topic you name least: its score with the cards behind it.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct TopicRecall {
    /// The topic tag.
    pub topic: String,
    /// [`TopicTally::score`].
    pub score: f64,
    /// Graded cards with the topic that named it.
    pub named: usize,
    /// Graded cards with the topic.
    pub seen: usize,
}

/// The rated topics scoring under [`WEAK_TOPIC_BELOW`], weakest first, then most seen, then
/// by name.
fn weak_topics(content: &Content, tallies: &[TopicTally]) -> Vec<TopicRecall> {
    let mut weak: Vec<TopicRecall> = content
        .topics
        .iter()
        .zip(tallies)
        .filter_map(|(topic, t)| {
            let score = t.score().filter(|&s| s < WEAK_TOPIC_BELOW)?;
            Some(TopicRecall {
                topic: topic.clone(),
                score,
                named: t.named,
                seen: t.seen,
            })
        })
        .collect();
    weak.sort_by(|a, b| {
        a.score
            .total_cmp(&b.score)
            .then(b.seen.cmp(&a.seen))
            .then_with(|| a.topic.cmp(&b.topic))
    });
    weak
}

/// The report: readiness and its trend over the company's most-asked problems, the study
/// counts over its 6-month list, and the flashcard figures over every list.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ScoreReport {
    /// When it was computed, Unix milliseconds.
    pub computed_at: i64,
    /// Readiness for the company's most-asked problems.
    pub readiness: Readiness,
    /// Readiness at the end of each recent day.
    pub trend: Trend,
    /// Mean topic score (F1) of the last 50 graded attempts, on any list.
    pub accuracy: Option<f64>,
    /// Graded (non-skip) attempts, on any list.
    pub graded: usize,
    /// Consecutive days with practice, ending today or yesterday.
    pub streak_days: usize,
    /// Cards per study state, over the 6-month list.
    pub counts: Counts,
    /// Cards graded per difficulty over the 6-month list, Easy to Hard.
    pub by_difficulty: Vec<DifficultyCoverage>,
    /// The topics you name least, over every graded card, weakest first.
    pub topics: Vec<TopicRecall>,
}

fn mean(values: impl IntoIterator<Item = f64>) -> Option<f64> {
    let (sum, n) = values
        .into_iter()
        .fold((0.0, 0_usize), |(sum, n), v| (sum + v, n + 1));
    (n > 0).then(|| sum / ratio(n, 1))
}

/// The process time zone: the `TZ` environment variable, else the system setting, else UTC.
#[must_use]
pub fn local_zone() -> TimeZone {
    TimeZone::try_system().unwrap_or(TimeZone::UTC)
}

/// Calendar day of a Unix-millisecond time in `tz`. Out-of-range times clamp to the
/// representable range.
#[must_use]
pub fn civil_day(at: i64, tz: &TimeZone) -> Date {
    let ts = Timestamp::from_millisecond(at).unwrap_or(if at < 0 {
        Timestamp::MIN
    } else {
        Timestamp::MAX
    });
    tz.to_datetime(ts).date()
}

/// The last millisecond of a calendar day in `tz` (the next day's start, less one), so
/// `civil_day(day_end(d)) == d` even across daylight-saving changes.
#[must_use]
pub fn day_end(day: Date, tz: &TimeZone) -> i64 {
    day.tomorrow()
        .and_then(|next| next.to_zoned(tz.clone()))
        .map_or(i64::MAX, |start| start.timestamp().as_millisecond() - 1)
}

/// The report for one company (or any) from what the learner did; `tz` is the server's
/// time zone, for calendar days.
#[must_use]
pub fn score_report(
    content: &Content,
    company: CompanyFilter,
    learner: Learner<'_>,
    now: i64,
    tz: &TimeZone,
) -> ScoreReport {
    let Learner {
        attempts, states, ..
    } = learner;
    let graded: Vec<&Attempt> = attempts.iter().filter(|a| a.grade != Grade::Skip).collect();
    let scope = content.list(ListId {
        company,
        period: Period::Months6,
    });

    let mut counts = Counts::default();
    let mut by_difficulty: Vec<DifficultyCoverage> = Difficulty::ALL
        .iter()
        .map(|&difficulty| DifficultyCoverage {
            difficulty,
            seen: 0,
            total: 0,
        })
        .collect();
    for entry in scope {
        let p = content.problem_at(entry);
        let state = states.get(&p.slug);
        match card_status(state, now) {
            CardStatus::Due => counts.due += 1,
            CardStatus::New => counts.new += 1,
            CardStatus::Later => {}
        }
        match state.and_then(|s| s.list) {
            Some(CardList::Again) => counts.again += 1,
            Some(CardList::Less) => counts.less += 1,
            None => {}
        }
        if let Some(group) = by_difficulty
            .iter_mut()
            .find(|d| d.difficulty == p.difficulty)
        {
            group.total += 1;
            group.seen += usize::from(state.is_some_and(|s| s.reviews > 0));
        }
    }

    let days = practice_days(attempts, learner.coding, tz);
    let list = readiness_list(content, company);
    let recent = &graded[graded.len().saturating_sub(RECENT_ATTEMPTS)..];
    ScoreReport {
        computed_at: now,
        readiness: readiness(&list, learner, now),
        trend: trend(&list, learner, &days, now, tz),
        accuracy: mean(recent.iter().map(|a| a.score.unwrap_or(0.0))),
        graded: graded.len(),
        streak_days: streak(&days, civil_day(now, tz)),
        counts,
        by_difficulty,
        topics: weak_topics(content, &topic_tallies(content, graded.iter().copied())),
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;
    use crate::coding::CodingLog;
    use crate::model::fixtures::{
        GOOGLE, META, T0, asked, attempt, attempt_scored, classic, companies, problem, with,
    };
    use crate::scheduler::{DAY, card_states};

    fn strings(items: &[&str]) -> Vec<String> {
        items.iter().map(|&s| s.to_owned()).collect()
    }

    /// p1 (Google 90, Meta 20, Array + Graph), p2 (Google 10, Easy, Tree), p500 (Meta only,
    /// Graph) and p900 (no company).
    fn content() -> Content {
        let mut p1 = with(problem(1), GOOGLE, Period::Months6, asked(1, 90.0));
        p1 = with(p1, META, Period::Months6, asked(2, 20.0));
        p1.topics = strings(&["Array", "Graph"]);
        let mut p2 = problem(2);
        p2.difficulty = Difficulty::Easy;
        p2.topics = strings(&["Tree"]);
        let mut p500 = with(classic(500), META, Period::Months6, asked(1, 80.0));
        p500.topics = strings(&["Graph"]);
        Content::new(
            companies(),
            vec![p1, p2, p500, classic(900)],
            HashMap::new(),
        )
    }

    fn report(log: &[Attempt], company: CompanyFilter, now: i64) -> ScoreReport {
        let states = card_states(log);
        let coding = CodingLog::new(TimeZone::UTC);
        let learner = Learner {
            attempts: log,
            states: &states,
            coding: &coding,
        };
        score_report(&content(), company, learner, now, &TimeZone::UTC)
    }

    const G: CompanyFilter = CompanyFilter::Company(GOOGLE);

    fn close(a: f64, b: f64) -> bool {
        (a - b).abs() < 1e-6
    }

    /// An attempt guessing these topics.
    fn guess(slug: &str, guessed: &[&str], at: i64) -> Attempt {
        let mut a = attempt_scored(slug, Grade::Good, at, Some(0.5));
        a.guessed = strings(guessed);
        a
    }

    #[test]
    fn scores_a_topic_guess_with_f1() {
        let result = score_topics(
            &strings(&["Array", "Graph"]),
            &strings(&["Array", "Hash Table"]),
        );
        assert_eq!(
            result,
            TopicResult {
                hits: strings(&["Array"]),
                missed: strings(&["Hash Table"]),
                extra: strings(&["Graph"]),
                score: 0.5,
            }
        );
        assert!(close(score_topics(&[], &[]).score, 0.0));
    }

    #[test]
    fn counts_the_six_month_list_and_grades_on_every_list() {
        let log = [
            attempt("p1", Grade::Less, T0),
            attempt("p500", Grade::Again, T0),
            attempt("p900", Grade::Good, T0),
            attempt("p2", Grade::Skip, T0),
        ];
        let google = report(&log, G, T0);
        // Google's list: p1 (on the less list) and p2 (skipped, so not due yet, nor new).
        assert_eq!(
            google.counts,
            Counts {
                due: 0,
                new: 0,
                again: 0,
                less: 1
            }
        );
        let seen: Vec<_> = google
            .by_difficulty
            .iter()
            .map(|d| (d.difficulty, d.seen, d.total))
            .collect();
        assert_eq!(
            seen,
            [
                (Difficulty::Easy, 0, 1),
                (Difficulty::Medium, 1, 1),
                (Difficulty::Hard, 0, 0)
            ]
        );
        // Grades and accuracy count every list; skips are no grades.
        assert_eq!(google.graded, 3);
        assert_eq!(google.accuracy, Some(1.0));
        let meta = report(&log, CompanyFilter::Company(META), T0);
        assert_eq!((meta.counts.again, meta.counts.less), (1, 1));
        assert_eq!(meta.graded, google.graded);
        let any = report(&log, CompanyFilter::Any, T0);
        assert_eq!(any.by_difficulty.iter().map(|d| d.total).sum::<usize>(), 3);
    }

    #[test]
    fn rates_a_topic_from_five_cards_counting_misses_and_false_alarms() {
        let tally = |named, seen, false_alarms| TopicTally {
            named,
            seen,
            false_alarms,
        };
        assert_eq!(tally(4, 4, 0).score(), None);
        assert_eq!(tally(0, 5, 0).score(), Some(0.0));
        assert!(close(tally(5, 5, 0).score().unwrap(), 1.0));
        // Named 2 of 9: 2 / (2 + 7/2).
        assert!(close(tally(2, 9, 0).score().unwrap(), 4.0 / 11.0));
        // Named every time, but also on 5 cards without it: 5 / (5 + 5/2).
        assert!(close(tally(5, 5, 5).score().unwrap(), 2.0 / 3.0));
    }

    #[test]
    fn lists_the_topics_named_least_weakest_first() {
        let mut log = Vec::new();
        for i in 0..5 {
            // Array named every time on p1, Graph never; Tree guessed where it is not.
            log.push(guess("p1", &["Array", "Tree"], T0 + i));
            // Graph named on p500 every time, Array guessed where it is not.
            log.push(guess("p500", &["Graph", "Array"], T0 + i));
        }
        // Tree, on p2, named once in four: too few cards to rate.
        for i in 0..4 {
            let guessed: &[&str] = if i == 0 { &["Tree"] } else { &[] };
            log.push(guess("p2", guessed, T0 + i));
        }
        let topics: Vec<_> = report(&log, G, T0 + DAY)
            .topics
            .iter()
            .map(|t| (t.topic.clone(), t.named, t.seen))
            .collect();
        // Graph: 5 of 10, 10 / (10 + 5) = 67%, not listed. Array: 5 of 5 but 5 false alarms,
        // 67%, not listed either. Only a weaker topic shows, so add misses on Array.
        assert!(topics.is_empty(), "{topics:?}");
        for i in 0..3 {
            log.push(guess("p1", &["Graph"], T0 + 10 + i));
        }
        let topics: Vec<_> = report(&log, G, T0 + DAY)
            .topics
            .iter()
            .map(|t| (t.topic.clone(), t.named, t.seen))
            .collect();
        // Array: 5 of 8, 5 false alarms: 10 / (10 + 3 + 5) = 56%.
        assert_eq!(topics, [("Array".to_owned(), 5, 8)]);
    }

    #[test]
    fn day_end_is_the_last_millisecond_of_the_calendar_day() {
        let utc = TimeZone::UTC;
        let day = civil_day(T0, &utc);
        assert_eq!(day.to_string(), "2026-01-01");
        assert_eq!(day_end(day, &utc), T0 + DAY - 1);
        // New York springs forward on 2026-03-08: a day of 23 hours.
        let ny = TimeZone::get("America/New_York").expect("zone");
        let spring = jiff::civil::date(2026, 3, 8);
        let end = day_end(spring, &ny);
        assert_eq!(civil_day(end, &ny), spring);
        assert_eq!(civil_day(end + 1, &ny), jiff::civil::date(2026, 3, 9));
        assert_eq!(
            end - day_end(jiff::civil::date(2026, 3, 7), &ny),
            23 * 3_600_000
        );
    }

    #[test]
    fn an_empty_log_reports_nothing_measured() {
        let report = report(&[], G, T0);
        assert_eq!((report.graded, report.streak_days), (0, 0));
        assert_eq!(report.accuracy, None);
        assert!(report.topics.is_empty());
        assert_eq!(report.readiness.score, None);
        assert_eq!(report.trend.practice_days, 0);
    }
}
