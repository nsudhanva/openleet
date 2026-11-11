//! The progress page's analytics beyond the flashcard report: coding progress over the
//! selected company's 6-month list, the shaky solves, the list's topic map, the activity
//! calendar and the days with practice behind it and the streak. Computed from memory: the
//! content, the attempt log and card states, and the coding log.

use std::collections::{BTreeMap, BTreeSet, HashSet};

use jiff::ToSpan;
use jiff::civil::{Date, Weekday};
use jiff::tz::TimeZone;
use serde::{Serialize, Serializer};

use crate::coding::{CodingLog, Failures, VerdictCounts};
use crate::content::Content;
use crate::lists::ListId;
use crate::model::{Attempt, CompanyFilter, Difficulty, Grade, MAX_TOPICS, Period, Problem};
use crate::scheduler::CardStates;
use crate::scorer::{TopicTally, civil_day, topic_tallies};

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
    /// Solved problems with no real failure before the first Accepted (compile errors and
    /// output limits do not count, as for shaky solves).
    pub first_try: usize,
    /// Submissions to the list's problems.
    pub submissions: u32,
    /// The failed verdicts before each problem's first Accepted (every one while unsolved),
    /// by kind.
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
    /// The topic's problems in the list.
    pub problems: usize,
    /// Of those, graded on a flashcard or solved.
    pub covered: usize,
    /// Of those, solved.
    pub solved: usize,
    /// Graded cards of the list's problems with the topic.
    pub graded: usize,
    /// How many of those named it; `None` below [`crate::scorer::MIN_TOPIC_CARDS`] graded.
    pub named: Option<usize>,
}

/// A date as JSON: "2026-11-10".
pub(crate) fn iso_date<S: Serializer>(date: &Date, serializer: S) -> Result<S::Ok, S::Error> {
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
    /// The list's topics, most problems first.
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
}

/// One piece of practice: a graded flashcard (a skip is none) or a judged submission.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Practice {
    Review,
    Submission,
}

/// Every piece of practice with its time: the graded attempts, then the submissions.
pub fn practice<'a>(
    attempts: &'a [Attempt],
    log: &'a CodingLog,
) -> impl Iterator<Item = (i64, Practice)> + 'a {
    let reviews = attempts
        .iter()
        .filter(|a| a.grade != Grade::Skip)
        .map(|a| (a.at, Practice::Review));
    let submissions = log.times().iter().map(|&at| (at, Practice::Submission));
    reviews.chain(submissions)
}

/// The calendar days in `tz` with any [`practice`]: the days the activity calendar shades.
#[must_use]
pub fn practice_days(attempts: &[Attempt], log: &CodingLog, tz: &TimeZone) -> BTreeSet<Date> {
    practice(attempts, log)
        .map(|(at, _)| civil_day(at, tz))
        .collect()
}

/// Consecutive days with practice ending `today`; today without practice yet does not break
/// a streak that ran through yesterday. Steps by calendar day, so daylight-saving days
/// count once.
#[must_use]
pub fn streak(days: &BTreeSet<Date>, today: Date) -> usize {
    let mut day = today;
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
    } = learner;
    let list = ListId {
        company,
        period: Period::Months6,
    };
    let problems: Vec<&'a Problem> = content.list_problems(list).collect();
    let slugs: HashSet<&str> = problems.iter().map(|p| p.slug.as_str()).collect();
    let in_list = |slug: &str| slugs.contains(slug);
    let mut shaky: Vec<ShakySolve<'a>> = problems
        .iter()
        .filter_map(|&p| {
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
    let graded = attempts
        .iter()
        .filter(|a| a.grade != Grade::Skip && in_list(&a.slug));
    Insights {
        coding: coding(&problems, log),
        shaky,
        shaky_elsewhere,
        topic_map: topic_map(
            content,
            &problems,
            states,
            log,
            &topic_tallies(content, graded),
        ),
        activity: activity(attempts, log, now, tz),
    }
}

fn coding(problems: &[&Problem], log: &CodingLog) -> Coding {
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
    let mut failed = VerdictCounts::default();
    for p in problems {
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
            first_try += usize::from(s.first_try());
            counts.merge(&s.counts);
            failed.merge(&s.before_accepted);
        }
    }
    Coding {
        by_difficulty,
        tried,
        first_try,
        submissions: crate::coding::VERDICTS.iter().map(|&v| counts.get(v)).sum(),
        failures: Failures::from(&failed),
    }
}

/// The list's topics with coverage, most problems first, ties by name. `tallies` are the
/// topics' tallies over the graded cards of the list's problems.
fn topic_map<'a>(
    content: &'a Content,
    problems: &[&Problem],
    states: &CardStates,
    log: &CodingLog,
    tallies: &[TopicTally],
) -> Vec<TopicRow<'a>> {
    #[derive(Default, Clone, Copy)]
    struct Tally {
        problems: usize,
        covered: usize,
        solved: usize,
    }
    let mut coverage = [Tally::default(); MAX_TOPICS];
    for p in problems {
        let solved = log.solved(&p.slug);
        let graded = states.get(&p.slug).is_some_and(|s| s.reviews > 0);
        for id in p.topic_set.iter() {
            let t = &mut coverage[usize::from(id)];
            t.problems += 1;
            t.covered += usize::from(graded || solved);
            t.solved += usize::from(solved);
        }
    }
    let mut rows: Vec<TopicRow<'a>> = content
        .topics
        .iter()
        .zip(coverage)
        .zip(tallies)
        .filter(|((_, t), _)| t.problems > 0)
        .map(|((topic, t), cards)| TopicRow {
            topic,
            problems: t.problems,
            covered: t.covered,
            solved: t.solved,
            graded: cards.seen,
            named: cards.score().map(|_| cards.named),
        })
        .collect();
    rows.sort_by(|a, b| b.problems.cmp(&a.problems).then(a.topic.cmp(b.topic)));
    rows
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
    for (at, kind) in practice(attempts, log) {
        let day = civil_day(at, tz);
        if day < start || day > today {
            continue;
        }
        let entry = days.entry(day).or_insert(ActiveDay {
            day,
            reviews: 0,
            submissions: 0,
        });
        match kind {
            Practice::Review => entry.reviews += 1,
            Practice::Submission => entry.submissions += 1,
        }
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
        let mut log = CodingLog::new(TimeZone::UTC);
        for (i, &(slug, verdict)) in (0_i64..).zip(submissions) {
            log.record(slug, T0 + i * DAY, verdict);
        }
        log
    }

    fn report<'a>(content: &'a Content, attempts: &[Attempt], log: &CodingLog) -> Insights<'a> {
        let states = card_states(attempts);
        insights(
            content,
            CompanyFilter::Company(GOOGLE),
            Learner {
                attempts,
                states: &states,
                coding: log,
            },
            T0 + 10 * DAY,
            &TimeZone::UTC,
        )
    }

    #[test]
    fn counts_solved_first_tries_and_failures_before_a_solve() {
        use Verdict::*;
        let content = content();
        let log = log(&[
            ("p1", Accepted),
            ("p1", WrongAnswer),
            ("p2", WrongAnswer),
            ("p2", CompileError),
            ("p2", Accepted),
            ("p3", TimeLimitExceeded),
            ("p4", CompileError),
            ("p4", Accepted),
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
                (Difficulty::Easy, 2, 2),
                (Difficulty::Medium, 0, 1),
                (Difficulty::Hard, 1, 1)
            ]
        );
        // p1 solved at once, p4 after only a compile error; p2 after a wrong answer. The
        // outside problem is not in the list.
        assert_eq!(
            (coding.tried, coding.first_try, coding.submissions),
            (4, 2, 8)
        );
        // Only failures before a problem's first Accepted (all of them while unsolved): p1's
        // wrong answer after its Accepted is left out.
        assert_eq!(
            (
                coding.failures.wrong_answer,
                coding.failures.compile_error,
                coding.failures.time_limit_exceeded
            ),
            (1, 2, 1)
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
    fn a_clean_solve_on_a_later_day_clears_the_list_and_the_shaky_plan_alike() {
        use Verdict::*;
        let content = content();
        // A day apart each: p1 solved again cleanly, p3 solved again after another failure.
        let log = log(&[
            ("p1", TimeLimitExceeded),
            ("p1", Accepted),
            ("p3", TimeLimitExceeded),
            ("p3", Accepted),
            ("p1", Accepted),
            ("p3", WrongAnswer),
            ("p3", Accepted),
        ]);
        let shaky: Vec<_> = report(&content, &[], &log)
            .shaky
            .iter()
            .map(|s| s.slug)
            .collect();
        assert_eq!(shaky, ["p3"]);
        let plan: Vec<_> = ["p1", "p3"]
            .into_iter()
            .filter(|slug| crate::plan::PlanStatus::Shaky.keeps(slug, &log))
            .collect();
        assert_eq!(plan, shaky);
    }

    #[test]
    fn maps_topics_by_problem_count_with_cards_named_on_the_list() {
        let content = content();
        let named_array = |slug: &str, at| {
            let mut a = attempt(slug, Grade::Good, at);
            a.guessed = vec!["Array".to_owned()];
            a
        };
        let mut attempts = vec![attempt("p4", Grade::Good, T0)];
        // Five graded cards of p3 name Array; the problem outside the list does not count.
        attempts.extend((1..=5).map(|i| named_array("p3", T0 + i)));
        attempts.push(named_array("outside", T0 + 6));
        let log = log(&[("p3", Verdict::Accepted)]);
        let map = report(&content, &attempts, &log).topic_map;
        let rows: Vec<_> = map
            .iter()
            .map(|t| (t.topic, t.problems, t.covered, t.solved, t.graded, t.named))
            .collect();
        // Array: p2 and p3; Graph: p1 and p2; Tree: p4, graded once, too few to rate.
        assert_eq!(
            rows,
            [
                ("Array", 2, 1, 1, 5, Some(5)),
                ("Graph", 2, 0, 0, 0, None),
                ("Tree", 1, 1, 0, 1, None),
            ]
        );
    }

    #[test]
    fn the_streak_counts_graded_cards_and_submissions_but_not_skips() {
        let tz = TimeZone::UTC;
        let today = civil_day(T0, &tz);
        let days = |attempts: &[Attempt], log: &CodingLog| practice_days(attempts, log, &tz);
        let none = CodingLog::new(TimeZone::UTC);
        assert_eq!(streak(&days(&[], &none), today), 0);
        // Graded two days back, only skipped yesterday: the skip breaks it.
        let skipped = [
            attempt("p1", Grade::Good, T0 - 2 * DAY),
            attempt("p1", Grade::Skip, T0 - DAY),
        ];
        assert_eq!(streak(&days(&skipped, &none), today), 0);
        // A submission yesterday fills the gap; today without practice yet does not break it.
        let mut submitted = CodingLog::new(TimeZone::UTC);
        submitted.record("p2", T0 - DAY + 5, Verdict::WrongAnswer);
        assert_eq!(streak(&days(&skipped, &submitted), today), 2);
        // A day with nothing in between ends it.
        assert_eq!(
            streak(&days(&skipped, &submitted), civil_day(T0 + DAY, &tz)),
            0
        );
        // Submissions alone make a streak.
        let mut only_code = CodingLog::new(TimeZone::UTC);
        for i in 0..3 {
            only_code.record("p1", T0 - i * DAY, Verdict::Accepted);
        }
        assert_eq!(streak(&days(&[], &only_code), today), 3);
        // The streak's days are the activity calendar's.
        let calendar: BTreeSet<Date> = activity(&skipped, &submitted, T0, &tz)
            .days
            .iter()
            .map(|d| d.day)
            .collect();
        assert_eq!(calendar, days(&skipped, &submitted));
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
