//! The progress page's analytics beyond the flashcard report: coding progress over the
//! selected company's 6-month list (the readiness list), the shaky solves, the list's topic
//! map and the activity calendar. Computed from memory: the content, the attempt log and
//! card states, the coding log and the report's topic recall.

use std::collections::BTreeMap;

use jiff::ToSpan;
use jiff::civil::{Date, Weekday};
use jiff::tz::TimeZone;
use serde::{Serialize, Serializer};

use crate::coding::{CodingLog, Failures, VerdictCounts};
use crate::content::Content;
use crate::lists::ListId;
use crate::model::{Attempt, CompanyFilter, Difficulty, Grade, MAX_TOPICS, Period, Problem};
use crate::scheduler::CardStates;
use crate::scorer::{TopicRecall, civil_day};

/// Weeks the activity calendar covers, ending with the current week.
pub const ACTIVITY_WEEKS: i64 = 26;

/// Solved problems of one difficulty, against the list's.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct SolvedCount {
    pub difficulty: Difficulty,
    pub solved: usize,
    pub total: usize,
}

/// Coding progress over the list.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Coding {
    /// Solved out of all, per difficulty, Easy to Hard.
    pub by_difficulty: Vec<SolvedCount>,
    /// Problems of the list with any submission.
    pub tried: usize,
    /// Solved problems whose first submission was Accepted.
    pub first_try: usize,
    /// Submissions to the list's problems.
    pub submissions: u32,
    /// Those submissions' failed verdicts, by kind.
    pub failures: Failures,
}

/// A problem solved only after failing: worth another try.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ShakySolve<'a> {
    pub id: u32,
    pub slug: &'a str,
    pub title: &'a str,
    pub difficulty: Difficulty,
    /// The failed verdicts before the first Accepted, by kind.
    pub failures: Failures,
    /// When the first Accepted came, Unix milliseconds.
    pub solved_at: i64,
}

/// One topic of the list, with how much of it the learner has covered.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct TopicRow<'a> {
    pub topic: &'a str,
    /// How much the company asks it: its frequency summed over the topic's problems, to the
    /// nearest whole number (it only ranks topics).
    pub weight: u32,
    /// The topic's problems in the list.
    pub problems: usize,
    /// Of those, graded on a flashcard or solved.
    pub covered: usize,
    /// Of those, solved.
    pub solved: usize,
    /// How often the learner named it on a card when it applied, to three decimals; `None`
    /// before any card with it was graded.
    pub recall: Option<f64>,
}

/// A date as JSON: "2026-11-10".
fn iso_date<S: Serializer>(date: &Date, serializer: S) -> Result<S::Ok, S::Error> {
    serializer.collect_str(date)
}

/// One day with practice.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ActiveDay {
    /// The calendar day, in the server's time zone.
    #[serde(serialize_with = "iso_date")]
    pub day: Date,
    /// Flashcards graded (skips left out).
    pub reviews: u32,
    /// Submissions judged.
    pub submissions: u32,
}

/// The activity calendar: the days from `start` (a Monday, [`ACTIVITY_WEEKS`] weeks back)
/// to `today`; only the days with practice are listed.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Activity {
    #[serde(serialize_with = "iso_date")]
    pub start: Date,
    #[serde(serialize_with = "iso_date")]
    pub today: Date,
    pub days: Vec<ActiveDay>,
}

/// Everything [`insights`] computes, as the report endpoint sends it.
#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Insights<'a> {
    pub coding: Coding,
    /// The list's shaky solves, newest first.
    pub shaky: Vec<ShakySolve<'a>>,
    /// Shaky solves outside the list.
    pub shaky_elsewhere: usize,
    /// The list's topics, most asked first.
    pub topic_map: Vec<TopicRow<'a>>,
    pub activity: Activity,
}

/// What the learner did, as the progress cache holds it.
#[derive(Debug, Clone, Copy)]
pub struct Learner<'a> {
    /// The attempt log, oldest first.
    pub attempts: &'a [Attempt],
    /// Card states replayed from it.
    pub states: &'a CardStates,
    /// Every judged submission.
    pub coding: &'a CodingLog,
    /// The report's topic recall.
    pub recall: &'a [TopicRecall],
}

/// The analytics for `company`'s 6-month list; `tz` is the server's time zone, for the
/// calendar.
#[must_use]
pub fn insights<'a>(
    content: &'a Content,
    company: CompanyFilter,
    learner: Learner<'_>,
    now: i64,
    tz: &TimeZone,
) -> Insights<'a> {
    let Learner {
        attempts,
        states,
        coding: log,
        recall,
    } = learner;
    let list = ListId {
        company,
        period: Period::Months6,
    };
    let problems: Vec<(&'a Problem, f32)> = content
        .list(list)
        .iter()
        .map(|e| (content.problem_at(e), e.frequency))
        .collect();
    let in_list = |slug: &str| problems.iter().any(|(p, _)| p.slug == slug);
    let mut shaky: Vec<ShakySolve<'a>> = problems
        .iter()
        .filter_map(|&(p, _)| {
            let submissions = log.problem(&p.slug).filter(|s| s.shaky())?;
            Some(ShakySolve {
                id: p.id,
                slug: &p.slug,
                title: &p.title,
                difficulty: p.difficulty,
                failures: Failures::from(&submissions.before_accepted),
                solved_at: submissions.accepted_at.unwrap_or_default(),
            })
        })
        .collect();
    shaky.sort_by(|a, b| b.solved_at.cmp(&a.solved_at).then(a.id.cmp(&b.id)));
    let shaky_elsewhere = log
        .problems()
        .filter(|(slug, s)| s.shaky() && !in_list(slug))
        .count();
    Insights {
        coding: coding(&problems, log),
        shaky,
        shaky_elsewhere,
        topic_map: topic_map(content, &problems, states, log, recall),
        activity: activity(attempts, log, now, tz),
    }
}

fn coding(problems: &[(&Problem, f32)], log: &CodingLog) -> Coding {
    let mut by_difficulty: Vec<SolvedCount> = Difficulty::ALL
        .iter()
        .map(|&difficulty| SolvedCount {
            difficulty,
            solved: 0,
            total: 0,
        })
        .collect();
    let (mut tried, mut first_try) = (0, 0);
    let mut counts = VerdictCounts::default();
    for (p, _) in problems {
        let group = by_difficulty
            .iter_mut()
            .find(|d| d.difficulty == p.difficulty);
        let submissions = log.problem(&p.slug);
        if let Some(group) = group {
            group.total += 1;
            group.solved += usize::from(submissions.is_some_and(|s| s.solved()));
        }
        if let Some(s) = submissions {
            tried += 1;
            first_try += usize::from(s.solved() && s.first_try());
            counts.merge(&s.counts);
        }
    }
    Coding {
        by_difficulty,
        tried,
        first_try,
        submissions: crate::coding::VERDICTS.iter().map(|&v| counts.get(v)).sum(),
        failures: Failures::from(&counts),
    }
}

/// The list's topics with coverage, ordered by how much the company asks each (its
/// frequency summed over the topic's problems), ties by name.
fn topic_map<'a>(
    content: &'a Content,
    problems: &[(&Problem, f32)],
    states: &CardStates,
    log: &CodingLog,
    recall: &[TopicRecall],
) -> Vec<TopicRow<'a>> {
    #[derive(Default, Clone, Copy)]
    struct Tally {
        weight: f32,
        problems: usize,
        covered: usize,
        solved: usize,
    }
    let mut tallies = [Tally::default(); MAX_TOPICS];
    for &(p, frequency) in problems {
        let solved = log.solved(&p.slug);
        let graded = states.get(&p.slug).is_some_and(|s| s.reviews > 0);
        for id in p.topic_set.iter() {
            let t = &mut tallies[usize::from(id)];
            t.weight += frequency;
            t.problems += 1;
            t.covered += usize::from(graded || solved);
            t.solved += usize::from(solved);
        }
    }
    let mut rows: Vec<TopicRow<'a>> = content
        .topics
        .iter()
        .zip(tallies)
        .filter(|(_, t)| t.problems > 0)
        .map(|(topic, t)| TopicRow {
            topic,
            weight: whole(t.weight),
            problems: t.problems,
            covered: t.covered,
            solved: t.solved,
            recall: recall
                .iter()
                .find(|r| r.topic == *topic)
                .map(|r| (r.recall * 1000.0).round() / 1000.0),
        })
        .collect();
    rows.sort_by(|a, b| b.weight.cmp(&a.weight).then(a.topic.cmp(b.topic)));
    rows
}

/// A non-negative sum of frequencies (0 to 100 each, a few thousand problems) as a whole
/// number.
#[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
fn whole(weight: f32) -> u32 {
    weight.max(0.0).round() as u32
}

/// Reviews and submissions per day over the last [`ACTIVITY_WEEKS`] weeks, in `tz`.
fn activity(attempts: &[Attempt], log: &CodingLog, now: i64, tz: &TimeZone) -> Activity {
    let today = civil_day(now, tz);
    let monday = today
        .checked_sub(i64::from(today.weekday().to_monday_zero_offset()).days())
        .unwrap_or(today);
    let start = monday
        .checked_sub(((ACTIVITY_WEEKS - 1) * 7).days())
        .unwrap_or(monday);
    let mut days: BTreeMap<Date, ActiveDay> = BTreeMap::new();
    let mut count = |at: i64, review: bool| {
        let day = civil_day(at, tz);
        if day < start || day > today {
            return;
        }
        let entry = days.entry(day).or_insert(ActiveDay {
            day,
            reviews: 0,
            submissions: 0,
        });
        if review {
            entry.reviews += 1;
        } else {
            entry.submissions += 1;
        }
    };
    for a in attempts.iter().filter(|a| a.grade != Grade::Skip) {
        count(a.at, true);
    }
    for &at in log.times() {
        count(at, false);
    }
    debug_assert_eq!(start.weekday(), Weekday::Monday);
    Activity {
        start,
        today,
        days: days.into_values().collect(),
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use openleet_proto::Verdict;

    use super::*;
    use crate::model::fixtures::{GOOGLE, T0, attempt, companies, problem};
    use crate::scheduler::card_states;

    const DAY: i64 = 86_400_000;

    /// Google 6 months, rank order (frequency 10 each, but p2 30): p1 Easy [Graph],
    /// p2 Hard [Graph, Array], p3 Medium [Array], p4 Easy [Tree].
    fn content() -> Content {
        let tagged = |rank, difficulty, topics: &[&str], frequency: f32| {
            let mut p = problem(rank);
            p.difficulty = difficulty;
            p.topics = topics.iter().map(|t| (*t).to_owned()).collect();
            if let Some(c) = p.companies.first_mut() {
                c.periods[2] = c.periods[2].map(|a| crate::model::Asked { frequency, ..a });
            }
            p
        };
        let outside = {
            let mut p = crate::model::fixtures::classic(9);
            p.slug = "outside".into();
            p
        };
        Content::new(
            companies(),
            vec![
                tagged(1, Difficulty::Easy, &["Graph"], 10.0),
                tagged(2, Difficulty::Hard, &["Graph", "Array"], 30.0),
                tagged(3, Difficulty::Medium, &["Array"], 10.0),
                tagged(4, Difficulty::Easy, &["Tree"], 10.0),
                outside,
            ],
            HashMap::new(),
        )
    }

    fn log(submissions: &[(&str, Verdict)]) -> CodingLog {
        let mut log = CodingLog::default();
        for (i, &(slug, verdict)) in (0_i64..).zip(submissions) {
            log.record(slug, T0 + i * DAY, verdict);
        }
        log
    }

    fn report<'a>(content: &'a Content, attempts: &[Attempt], log: &CodingLog) -> Insights<'a> {
        let recall = vec![TopicRecall {
            topic: "Array".into(),
            recall: 0.5,
            seen: 2,
        }];
        let states = card_states(attempts);
        insights(
            content,
            CompanyFilter::Company(GOOGLE),
            Learner {
                attempts,
                states: &states,
                coding: log,
                recall: &recall,
            },
            T0 + 10 * DAY,
            &TimeZone::UTC,
        )
    }

    #[test]
    fn counts_solved_first_tries_and_failures_over_the_list() {
        use Verdict::*;
        let content = content();
        let log = log(&[
            ("p1", Accepted),
            ("p2", WrongAnswer),
            ("p2", CompileError),
            ("p2", Accepted),
            ("p3", TimeLimitExceeded),
            ("outside", Accepted),
        ]);
        let coding = report(&content, &[], &log).coding;
        let solved: Vec<_> = coding
            .by_difficulty
            .iter()
            .map(|d| (d.difficulty, d.solved, d.total))
            .collect();
        assert_eq!(
            solved,
            [
                (Difficulty::Easy, 1, 2),
                (Difficulty::Medium, 0, 1),
                (Difficulty::Hard, 1, 1)
            ]
        );
        // p1 solved at once; p2 only on its third; the outside problem is not in the list.
        assert_eq!(
            (coding.tried, coding.first_try, coding.submissions),
            (3, 1, 5)
        );
        assert_eq!(
            (
                coding.failures.wrong_answer,
                coding.failures.compile_error,
                coding.failures.time_limit_exceeded
            ),
            (1, 1, 1)
        );
    }

    #[test]
    fn lists_the_shaky_solves_newest_first() {
        use Verdict::*;
        let content = content();
        let log = log(&[
            ("p1", TimeLimitExceeded),
            ("p1", Accepted),
            ("p2", CompileError),
            ("p2", CompileError),
            ("p2", WrongAnswer),
            ("p2", Accepted),
            ("p3", WrongAnswer),
            ("p3", RuntimeError),
            ("p3", Accepted),
            ("outside", TimeLimitExceeded),
            ("outside", Accepted),
        ]);
        let insights = report(&content, &[], &log);
        let shaky: Vec<_> = insights.shaky.iter().map(|s| s.slug).collect();
        // p2's compile errors do not count; p3 (two real failures) came after p1 (a TLE).
        assert_eq!(shaky, ["p3", "p1"]);
        assert_eq!(insights.shaky[0].failures.runtime_error, 1);
        assert_eq!(insights.shaky_elsewhere, 1);
    }

    #[test]
    fn maps_topics_by_how_much_the_company_asks_them() {
        let content = content();
        let attempts = [attempt("p4", Grade::Good, T0)];
        let log = log(&[("p3", Verdict::Accepted)]);
        let map = report(&content, &attempts, &log).topic_map;
        let rows: Vec<_> = map
            .iter()
            .map(|t| (t.topic, t.weight, t.problems, t.covered, t.solved, t.recall))
            .collect();
        // Array: p2 (30) and p3 (10); Graph: p1 (10) and p2 (30); Tree: p4. Ties by name.
        assert_eq!(
            rows,
            [
                ("Array", 40, 2, 1, 1, Some(0.5)),
                ("Graph", 40, 2, 0, 0, None),
                ("Tree", 10, 1, 1, 0, None),
            ]
        );
    }

    #[test]
    fn counts_days_in_the_time_zone_over_twenty_six_weeks() {
        // 2026-01-01 is a Thursday. 23:30 UTC on the 1st is the 2nd in Tokyo.
        let late = T0 + 23 * 3_600_000 + 30 * 60_000;
        let attempts = [
            attempt("p1", Grade::Good, late),
            attempt("p2", Grade::Skip, late),
            attempt("p3", Grade::Again, T0 - 400 * DAY),
        ];
        let mut log = CodingLog::default();
        log.record("p1", late, Verdict::Accepted);
        log.record("p1", T0 + 10 * DAY, Verdict::Accepted);
        let at = |tz: &TimeZone| activity(&attempts, &log, T0 + 10 * DAY, tz);
        let utc = at(&TimeZone::UTC);
        assert_eq!(utc.today.to_string(), "2026-01-11");
        assert_eq!(utc.start.weekday(), Weekday::Monday);
        assert_eq!(utc.start.to_string(), "2025-07-14");
        let days: Vec<_> = utc
            .days
            .iter()
            .map(|d| (d.day.to_string(), d.reviews, d.submissions))
            .collect();
        // The skip is no review; the attempt 400 days back is before the calendar.
        assert_eq!(
            days,
            [
                ("2026-01-01".to_owned(), 1, 1),
                ("2026-01-11".to_owned(), 0, 1)
            ]
        );
        let tokyo = TimeZone::get("Asia/Tokyo").expect("zone");
        assert_eq!(at(&tokyo).days[0].day.to_string(), "2026-01-02");
        let json = serde_json::to_value(&utc).expect("json");
        assert_eq!(
            json["days"][0],
            serde_json::json!({"day": "2026-01-01", "reviews": 1, "submissions": 1})
        );
    }
}
