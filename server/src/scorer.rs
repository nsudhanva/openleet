//! Topic-guess scoring and the readiness report.
//!
//! The report is company-scoped: readiness, coverage, `by_difficulty` and the due/new/again/less
//! counts only count the company's 6-month list. Topic recall, accuracy and the streak use
//! every attempt.

use std::collections::{HashMap, HashSet};

use jiff::Timestamp;
use jiff::civil::Date;
use jiff::tz::TimeZone;
use serde::Serialize;

use crate::content::Content;
use crate::lists::ListId;
use crate::model::{Attempt, CompanyFilter, Difficulty, Grade, Period, Problem};
use crate::scheduler::{CardList, CardState, CardStates, CardStatus, DAY, INTERVALS, card_status};

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

/// Weight of each grade in an attempt's quality.
const fn grade_value(grade: Grade) -> Option<f64> {
    match grade {
        Grade::Again => Some(0.0),
        Grade::Good => Some(0.8),
        Grade::Less => Some(1.0),
        Grade::Skip => None,
    }
}
/// Each hint opened keeps this share of the topic recall.
const HINT_DISCOUNT: f64 = 0.75;
/// Accuracy averages this many most recent graded attempts.
const RECENT_ATTEMPTS: usize = 50;

/// How well a graded attempt went: half topic recall (each hint opened costs a quarter of it),
/// half the learner's own grade. `None` for skips.
fn quality(attempt: &Attempt) -> Option<f64> {
    let grade = grade_value(attempt.grade)?;
    let hints = i32::try_from(attempt.hints).unwrap_or(i32::MAX);
    let recall = attempt.score.unwrap_or(0.0) * HINT_DISCOUNT.powi(hints);
    Some(0.5 * recall + 0.5 * grade)
}

/// Memory fades between reviews: at the card's own interval, retention is ~70%.
/// Half-life is twice the box interval, never less than a day.
fn retention(state: &CardState, now: i64) -> f64 {
    let half_life = (2 * INTERVALS[state.box_]).max(DAY);
    0.5_f64.powf(millis(0.max(now - state.last_at)) / millis(half_life))
}

/// Lossless for any realistic span (below 2^53 ms, about 285,000 years).
#[allow(clippy::cast_precision_loss)]
const fn millis(ms: i64) -> f64 {
    ms as f64
}

/// `num / den` as a float; counts here are far below 2^53.
#[allow(clippy::cast_precision_loss)]
fn ratio(num: usize, den: usize) -> f64 {
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

/// Mastery of one difficulty, over the selected company's 6-month list.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct DifficultyMastery {
    /// The difficulty.
    pub difficulty: Difficulty,
    /// Mean mastery over every problem of this difficulty, 0..1.
    pub mastery: f64,
    /// Problems graded at least once.
    pub seen: usize,
    /// Problems of this difficulty.
    pub total: usize,
}

/// How often the learner named a topic when it applied.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct TopicRecall {
    /// The topic tag.
    pub topic: String,
    /// Share of graded attempts on tagged problems that named it.
    pub recall: f64,
    /// Graded attempts on problems with this tag.
    pub seen: usize,
}

/// The readiness report.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ScoreReport {
    /// When it was computed, Unix milliseconds.
    pub computed_at: i64,
    /// Mastery weighted by the selected company's 6-month frequency, 0..1.
    pub readiness: f64,
    /// Share of the selected company's 6-month list graded at least once.
    pub coverage: f64,
    /// Mean topic score over the last 50 graded attempts.
    pub accuracy: Option<f64>,
    /// Graded (non-skip) attempts.
    pub graded: usize,
    /// Consecutive days with practice, ending today or yesterday.
    pub streak_days: usize,
    /// Cards per study state.
    pub counts: Counts,
    /// Mastery per difficulty, Easy to Hard.
    pub by_difficulty: Vec<DifficultyMastery>,
    /// Recall per topic, weakest first.
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

/// Calendar day in the process time zone (set `TZ`), such as "2026-10-28".
#[must_use]
pub fn day_key(at: i64) -> String {
    civil_day(at, &local_zone()).to_string()
}

/// Consecutive calendar days with an attempt, ending today; today without practice yet does
/// not break a streak that ran through yesterday. Steps by calendar day, not 24 hours, so
/// daylight-saving days count once.
fn streak(attempts: &[Attempt], now: i64) -> usize {
    let tz = local_zone();
    let days: HashSet<Date> = attempts.iter().map(|a| civil_day(a.at, &tz)).collect();
    let mut day = civil_day(now, &tz);
    if !days.contains(&day) {
        let Ok(yesterday) = day.yesterday() else {
            return 0;
        };
        day = yesterday;
    }
    let mut count = 0;
    while days.contains(&day) {
        count += 1;
        match day.yesterday() {
            Ok(prev) => day = prev,
            Err(_) => break,
        }
    }
    count
}

/// Mastery per attempted slug: an exponential moving average of attempt quality (latest
/// weighted most), faded by retention since the last attempt.
fn masteries<'a>(attempts: &'a [Attempt], states: &CardStates, now: i64) -> HashMap<&'a str, f64> {
    let mut averages: HashMap<&str, f64> = HashMap::new();
    for attempt in attempts {
        let Some(q) = quality(attempt) else { continue };
        averages
            .entry(attempt.slug.as_str())
            .and_modify(|avg| *avg = f64::midpoint(*avg, q))
            .or_insert(q);
    }
    averages.retain(|slug, average| match states.get(*slug) {
        Some(state) => {
            *average *= retention(state, now);
            true
        }
        None => false,
    });
    averages
}

/// Recall per topic over every graded attempt, weakest first, then most seen first; ties keep
/// the order topics were first met.
fn topic_recall(content: &Content, graded: &[&Attempt]) -> Vec<TopicRecall> {
    let mut index: HashMap<&str, usize> = HashMap::new();
    let mut tally: Vec<(&str, usize, usize)> = Vec::new();
    for attempt in graded {
        let Some(problem) = content.problem(&attempt.slug) else {
            continue;
        };
        for topic in &problem.topics {
            let i = *index.entry(topic).or_insert_with(|| {
                tally.push((topic, 0, 0));
                tally.len() - 1
            });
            let entry = &mut tally[i];
            entry.2 += 1;
            if attempt.guessed.iter().any(|g| g == topic) {
                entry.1 += 1;
            }
        }
    }
    let mut result: Vec<TopicRecall> = tally
        .into_iter()
        .map(|(topic, hit, seen)| TopicRecall {
            topic: topic.to_owned(),
            recall: ratio(hit, seen),
            seen,
        })
        .collect();
    result.sort_by(|a, b| a.recall.total_cmp(&b.recall).then(b.seen.cmp(&a.seen)));
    result
}

/// The report for one company (or any) from the attempt log (oldest first) and the card
/// states replayed from it. Readiness, coverage, `by_difficulty` and counts cover the
/// company's 6-month list, weighted by its 6-month frequency.
#[must_use]
pub fn score_report(
    content: &Content,
    company: CompanyFilter,
    attempts: &[Attempt],
    states: &CardStates,
    now: i64,
) -> ScoreReport {
    let mastery = masteries(attempts, states, now);
    let mastery_of = |p: &Problem| mastery.get(p.slug.as_str()).copied();
    let graded: Vec<&Attempt> = attempts.iter().filter(|a| a.grade != Grade::Skip).collect();
    let scope = content.list(ListId {
        company,
        period: Period::Months6,
    });

    let mut counts = Counts::default();
    let (mut weight, mut weighted, mut seen) = (0.0, 0.0, 0);
    let mut by_difficulty: Vec<DifficultyMastery> = Difficulty::ALL
        .iter()
        .map(|&difficulty| DifficultyMastery {
            difficulty,
            mastery: 0.0,
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
        let frequency = f64::from(entry.frequency);
        weight += frequency;
        let group = by_difficulty
            .iter_mut()
            .find(|d| d.difficulty == p.difficulty);
        if let Some(group) = group {
            group.total += 1;
            if let Some(m) = mastery_of(p) {
                group.mastery += m;
                group.seen += 1;
            }
        }
        if let Some(m) = mastery_of(p) {
            weighted += frequency * m;
            seen += 1;
        }
    }
    for group in &mut by_difficulty {
        // The sum so far becomes the mean over every problem of the group.
        group.mastery = if group.total == 0 {
            0.0
        } else {
            group.mastery / ratio(group.total, 1)
        };
    }

    let recent = &graded[graded.len().saturating_sub(RECENT_ATTEMPTS)..];
    ScoreReport {
        computed_at: now,
        readiness: if weight > 0.0 { weighted / weight } else { 0.0 },
        coverage: if scope.is_empty() {
            0.0
        } else {
            ratio(seen, scope.len())
        },
        accuracy: mean(recent.iter().map(|a| a.score.unwrap_or(0.0))),
        graded: graded.len(),
        streak_days: streak(attempts, now),
        counts,
        by_difficulty,
        topics: topic_recall(content, &graded),
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;
    use crate::model::fixtures::{
        GOOGLE, META, T0, asked, attempt, attempt_scored, classic, companies, problem, with,
    };
    use crate::scheduler::card_states;

    fn strings(items: &[&str]) -> Vec<String> {
        items.iter().map(|&s| s.to_owned()).collect()
    }

    /// p1 (Google 90, Meta 20, Array + Graph), p2 (Google 10, Easy), p500 (Meta only, Graph)
    /// and p900 (no company).
    fn content() -> Content {
        let mut p1 = with(problem(1), GOOGLE, Period::Months6, asked(1, 90.0));
        p1 = with(p1, META, Period::Months6, asked(2, 20.0));
        p1.topics = strings(&["Array", "Graph"]);
        let mut p2 = problem(2);
        p2.difficulty = Difficulty::Easy;
        let mut p500 = with(classic(500), META, Period::Months6, asked(1, 80.0));
        p500.topics = strings(&["Graph"]);
        Content::new(
            companies(),
            vec![p1, p2, p500, classic(900)],
            HashMap::new(),
        )
    }

    fn report(log: &[Attempt], company: CompanyFilter, now: i64) -> ScoreReport {
        score_report(&content(), company, log, &card_states(log), now)
    }

    const G: CompanyFilter = CompanyFilter::Company(GOOGLE);

    fn close(a: f64, b: f64) -> bool {
        (a - b).abs() < 1e-6
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
    fn weights_readiness_by_frequency_discounts_hints_and_decays() {
        let frequent = report(&[attempt("p1", Grade::Less, T0)], G, T0);
        assert!(close(frequent.readiness, 0.9));
        assert!(close(frequent.coverage, 0.5));
        let mut hinted_attempt = attempt("p1", Grade::Less, T0);
        hinted_attempt.hints = 1;
        let hinted = report(&[hinted_attempt], G, T0);
        assert!(hinted.readiness < frequent.readiness);
        let later = report(&[attempt("p1", Grade::Less, T0)], G, T0 + 30 * DAY);
        assert!(later.readiness < frequent.readiness);
    }

    #[test]
    fn counts_streaks_lists_and_the_weakest_topics() {
        let mut answer = attempt_scored("p1", Grade::Again, T0, Some(0.67));
        answer.guessed = strings(&["Array"]);
        let report = report(&[attempt("p2", Grade::Skip, T0 - DAY), answer], G, T0);
        assert_eq!(report.graded, 1);
        assert_eq!(report.streak_days, 2);
        // The day-old skip is past its delay, so it counts as new again.
        assert_eq!((report.counts.again, report.counts.new), (1, 1));
        let topics: Vec<_> = report
            .topics
            .iter()
            .map(|t| (t.topic.as_str(), t.recall))
            .collect();
        assert_eq!(topics, [("Graph", 0.0), ("Array", 1.0)]);
    }

    #[test]
    fn streak_allows_a_gap_today_but_not_before() {
        let log = [
            attempt("p1", Grade::Good, T0 - 2 * DAY),
            attempt("p1", Grade::Good, T0 - DAY),
        ];
        assert_eq!(report(&log, G, T0).streak_days, 2);
        assert_eq!(report(&log, G, T0 + DAY).streak_days, 0);
    }

    #[test]
    fn readiness_is_scoped_to_the_company_six_month_list() {
        let log = [
            attempt("p1", Grade::Less, T0),
            attempt("p500", Grade::Again, T0),
            attempt("p900", Grade::Good, T0),
        ];
        let google = report(&log, G, T0);
        // Google: p1 (90, mastered) and p2 (10); p500 and p900 are not in its list.
        assert!(close(google.readiness, 0.9));
        assert!(close(google.coverage, 0.5));
        assert_eq!(
            google.counts,
            Counts {
                due: 0,
                new: 1,
                again: 0,
                less: 1
            }
        );
        let medium = &google.by_difficulty[1];
        assert_eq!(
            (medium.difficulty, medium.seen, medium.total),
            (Difficulty::Medium, 1, 1)
        );
        // Graded attempts, accuracy and topics stay global.
        assert_eq!(google.graded, 3);
        let graph = google
            .topics
            .iter()
            .find(|t| t.topic == "Graph")
            .map(|t| t.seen);
        assert_eq!(graph, Some(2));

        // Meta: p1 (20, mastery 1) and p500 (80, an "again" with score 1: quality 0.5).
        let meta = report(&log, CompanyFilter::Company(META), T0);
        assert!(close(meta.readiness, 0.2 * 1.0 + 0.8 * 0.5));
        assert!(close(meta.coverage, 1.0));
        assert_eq!(
            meta.counts,
            Counts {
                due: 0,
                new: 0,
                again: 1,
                less: 1
            }
        );
        assert_eq!(meta.graded, google.graded);

        // Any: p1 weighted by its best (90), p2 (10), p500 (80).
        let any = report(&log, CompanyFilter::Any, T0);
        assert!(close(any.readiness, (90.0 + 80.0 * 0.5) / 180.0));
        assert!(close(any.coverage, 2.0 / 3.0));
    }

    #[test]
    fn day_keys_are_iso_dates() {
        let key = day_key(T0);
        assert_eq!(key.len(), 10);
        assert!(key.starts_with("2025-12-3") || key.starts_with("2026-01-0"));
        let utc = civil_day(T0, &TimeZone::UTC);
        assert_eq!(utc.to_string(), "2026-01-01");
    }
}
