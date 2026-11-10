//! Practice plans: a problem list, a filter over it, which of its problems still count (the
//! status) and an order. A plan is never curated: it is built on the fly from the content
//! (company lists, topics, difficulty) and the learner's submissions, and names the next
//! problem to solve.
//!
//! Topics stay hidden unless asked for: a plan's next problem carries no topics, and only the
//! pivots, offered after the current problem is solved, name the current problem's topics.

use serde::Serialize;

use crate::coding::CodingLog;

use crate::content::{ANY_COMPANY, Content};
use crate::lists::{ListEntry, ListId, ProblemFilter};
use crate::model::{CompanyFilter, Difficulty, Period, Problem, TopicId, wire_enum};

wire_enum! {
    /// Which problems of a plan are still to do.
    #[derive(Default)]
    PlanStatus: "status" {
        /// No accepted submission yet (the default).
        #[default]
        Unsolved = "unsolved",
        /// No submission at all.
        Untried = "untried",
        /// Solved, but shakily: after two or more failed submissions, or a time limit.
        Shaky = "shaky",
        /// Every problem, solved or not.
        All = "all",
    }
}

wire_enum! {
    /// The order a plan walks its problems in.
    #[derive(Default)]
    PlanOrder: "order" {
        /// List order: the company's rank, or the number for LC 1–1000 (the default).
        #[default]
        Rank = "rank",
        /// LeetCode number.
        Number = "number",
        /// Easy, then Medium, then Hard; list order within each.
        EasyFirst = "easy-first",
        /// A shuffle seeded by the plan's list and filter, so it is the same on every request.
        Random = "random",
    }
}

wire_enum! {
    /// How a pivot differs from the plan it was offered from.
    PivotKind: "pivot" {
        /// Only problems with one of the solved problem's topics.
        Topic = "topic",
        /// The plan's list with no topic filter.
        List = "list",
        /// One difficulty above the solved problem's.
        Harder = "harder",
        /// The learner's weakest topic, from the readiness report.
        Weakest = "weakest",
    }
}

/// Most pivots offered after a solve.
pub const MAX_PIVOTS: usize = 4;

/// What the learner has done in the judge: every submission, aggregated per problem.
pub type Marks<'a> = &'a CodingLog;

impl PlanStatus {
    /// Whether a problem still counts under this status.
    #[must_use]
    pub fn keeps(self, slug: &str, marks: Marks<'_>) -> bool {
        match self {
            Self::Unsolved => !marks.solved(slug),
            Self::Untried => !marks.tried(slug),
            Self::Shaky => marks.shaky(slug),
            Self::All => true,
        }
    }

    const fn label(self) -> Option<&'static str> {
        match self {
            Self::Unsolved => Some("Unsolved"),
            Self::Untried => Some("Untried"),
            Self::Shaky => Some("Shaky solves"),
            Self::All => None,
        }
    }
}

impl PlanOrder {
    const fn label(self) -> Option<&'static str> {
        match self {
            Self::Rank => None,
            Self::Number => Some("By number"),
            Self::EasyFirst => Some("Easy first"),
            Self::Random => Some("Shuffled"),
        }
    }
}

/// Easy 0, Medium 1, Hard 2.
const fn level(difficulty: Difficulty) -> u8 {
    match difficulty {
        Difficulty::Easy => 0,
        Difficulty::Medium => 1,
        Difficulty::Hard => 2,
    }
}

/// The difficulty one above, or `None` for Hard.
const fn harder(difficulty: Difficulty) -> Option<Difficulty> {
    match difficulty {
        Difficulty::Easy => Some(Difficulty::Medium),
        Difficulty::Medium => Some(Difficulty::Hard),
        Difficulty::Hard => None,
    }
}

/// 64-bit FNV-1a: a hash that is the same on every build and platform.
fn fnv1a(text: &str) -> u64 {
    text.bytes().fold(0xcbf2_9ce4_8422_2325, |hash, b| {
        (hash ^ u64::from(b)).wrapping_mul(0x0000_0100_0000_01b3)
    })
}

/// SplitMix64's finalizer: spreads a seed mixed with a problem number over 64 bits.
const fn mix(mut x: u64) -> u64 {
    x = (x ^ (x >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
    x = (x ^ (x >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
    x ^ (x >> 31)
}

/// A practice plan.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Plan {
    /// Which list.
    pub list: ListId,
    /// Which problems of it.
    pub filter: ProblemFilter,
    /// Which of those are still to do.
    pub status: PlanStatus,
    /// In which order.
    pub order: PlanOrder,
}

impl Plan {
    /// The plan's problems (status ignored), in its order.
    #[must_use]
    pub fn entries<'a>(&self, content: &'a Content) -> Vec<&'a ListEntry> {
        let mut entries: Vec<&ListEntry> = content
            .list(self.list)
            .iter()
            .filter(|e| self.filter.matches(content.problem_at(e)))
            .collect();
        let problem = |e: &ListEntry| content.problem_at(e);
        match self.order {
            PlanOrder::Rank => {}
            PlanOrder::Number => entries.sort_by_key(|e| problem(e).id),
            // Stable, so each difficulty keeps list order.
            PlanOrder::EasyFirst => entries.sort_by_key(|e| level(problem(e).difficulty)),
            PlanOrder::Random => {
                let seed = self.seed(content);
                entries.sort_by_key(|e| (mix(seed ^ u64::from(problem(e).id)), problem(e).id));
            }
        }
        entries
    }

    /// The shuffle's seed: the list and filter, so changing the status keeps the order.
    fn seed(&self, content: &Content) -> u64 {
        let view = self.view(content);
        fnv1a(&format!(
            "{}|{}|{}|{}",
            view.company,
            view.period,
            view.topic.unwrap_or_default(),
            view.difficulty.map_or("", Difficulty::as_str),
        ))
    }

    /// "Google · 6 months · Two Pointers · Unsolved": what the plan holds, defaults left out.
    #[must_use]
    pub fn label(&self, content: &Content) -> String {
        let mut parts: Vec<&str> = Vec::new();
        if self.list.period != Period::Lc1000 {
            parts.push(match self.list.company {
                CompanyFilter::Any => "Any company",
                CompanyFilter::Company(id) => &content.companies.get(id).name,
            });
        }
        parts.push(self.list.period.label());
        if let Some(topic) = self.topic_name(content) {
            parts.push(topic);
        }
        if let Some(difficulty) = self.filter.difficulty {
            parts.push(difficulty.as_str());
        }
        parts.extend(self.status.label());
        parts.extend(self.order.label());
        parts.join(" · ")
    }

    fn topic_name<'a>(&self, content: &'a Content) -> Option<&'a str> {
        topic_name(content, self.filter.topic?)
    }

    /// The plan as JSON, with its label.
    #[must_use]
    pub fn view<'a>(&self, content: &'a Content) -> PlanView<'a> {
        PlanView {
            company: match self.list.company {
                CompanyFilter::Any => ANY_COMPANY,
                CompanyFilter::Company(id) => &content.companies.get(id).slug,
            },
            period: self.list.period,
            topic: self.topic_name(content),
            difficulty: self.filter.difficulty,
            status: self.status,
            order: self.order,
            label: String::new(),
        }
    }

    /// [`Plan::view`] with the label filled in.
    #[must_use]
    pub fn labeled<'a>(&self, content: &'a Content) -> PlanView<'a> {
        PlanView {
            label: self.label(content),
            ..self.view(content)
        }
    }

    fn with_filter(self, topic: Option<TopicId>, difficulty: Option<Difficulty>) -> Self {
        Self {
            filter: ProblemFilter { topic, difficulty },
            ..self
        }
    }
}

fn topic_name(content: &Content, id: TopicId) -> Option<&str> {
    content.topics.get(usize::from(id)).map(String::as_str)
}

/// A plan in its JSON (and URL) shape: the query values that rebuild it.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct PlanView<'a> {
    /// A company slug or "any".
    pub company: &'a str,
    /// The list's period.
    pub period: Period,
    /// The topic filter, by name.
    pub topic: Option<&'a str>,
    /// The difficulty filter.
    pub difficulty: Option<Difficulty>,
    /// Which problems still count.
    pub status: PlanStatus,
    /// The order.
    pub order: PlanOrder,
    /// What it holds, in words; empty when not asked for.
    #[serde(skip_serializing_if = "String::is_empty")]
    pub label: String,
}

/// The problem a plan offers next. No topics: they would give away the guess.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct NextProblem<'a> {
    /// LeetCode number.
    pub id: u32,
    /// Slug.
    pub slug: &'a str,
    /// Title.
    pub title: &'a str,
    /// Difficulty.
    pub difficulty: Difficulty,
    /// Rank in the plan's list.
    pub rank: u32,
    /// Whether it needs LeetCode Premium.
    pub premium: bool,
}

impl<'a> NextProblem<'a> {
    fn of(problem: &'a Problem, entry: &ListEntry) -> Self {
        Self {
            id: problem.id,
            slug: &problem.slug,
            title: &problem.title,
            difficulty: problem.difficulty,
            rank: entry.rank,
            premium: problem.premium,
        }
    }
}

/// How much of a plan is solved, whatever its status.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub struct PlanProgress {
    /// Problems of the plan with an accepted submission.
    pub solved: usize,
    /// Problems of the plan.
    pub total: usize,
}

/// A plan's progress and next problem, computed from its ordered entries.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Walk<'a> {
    /// The problem after `after` that still counts, wrapping to the start; `None` when no
    /// problem but `after` counts.
    pub next: Option<NextProblem<'a>>,
    /// Solved out of all.
    pub progress: PlanProgress,
}

/// Walks a plan: its next problem after `after` (from the start when `None` or not in the
/// plan) and its progress.
#[must_use]
pub fn walk<'a>(
    content: &'a Content,
    plan: &Plan,
    after: Option<&str>,
    marks: Marks<'_>,
) -> Walk<'a> {
    let entries = plan.entries(content);
    let solved = entries
        .iter()
        .filter(|e| marks.solved(&content.problem_at(e).slug))
        .count();
    let start = after
        .and_then(|slug| {
            entries
                .iter()
                .position(|e| content.problem_at(e).slug == slug)
        })
        .map_or(0, |i| i + 1);
    let next = entries
        .iter()
        .cycle()
        .skip(start)
        .take(entries.len())
        .map(|e| (content.problem_at(e), *e))
        .find(|(p, _)| Some(p.slug.as_str()) != after && plan.status.keeps(&p.slug, marks))
        .map(|(p, e)| NextProblem::of(p, e));
    Walk {
        next,
        progress: PlanProgress {
            solved,
            total: entries.len(),
        },
    }
}

/// Another plan offered after a solve, with its next problem.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Pivot<'a> {
    /// How it differs from the plan.
    pub kind: PivotKind,
    /// The other plan, labeled.
    pub plan: PlanView<'a>,
    /// Its next problem.
    pub next: NextProblem<'a>,
}

/// `GET /api/next`: a plan, its next problem and progress, and the pivots.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct NextPage<'a> {
    /// The plan, labeled.
    pub plan: PlanView<'a>,
    /// Its next problem; `None` when the plan has no problem left to do.
    pub next: Option<NextProblem<'a>>,
    /// Solved out of all.
    pub progress: PlanProgress,
    /// Up to [`MAX_PIVOTS`] other plans from `current`: one per topic of it (as many as there
    /// is room for), its list with no topic, one difficulty harder, and the weakest topic.
    pub pivots: Vec<Pivot<'a>>,
}

/// The plan's next problem after `current` (from the start without one), its progress and
/// the pivots from `current`. `weakest` is the learner's weakest topic, if any.
#[must_use]
pub fn next_page<'a>(
    content: &'a Content,
    plan: &Plan,
    current: Option<&Problem>,
    marks: Marks<'_>,
    weakest: Option<&str>,
) -> NextPage<'a> {
    let after = current.map(|p| p.slug.as_str());
    let main = walk(content, plan, after, marks);
    let pivots = current.map_or_else(Vec::new, |problem| {
        pivots(content, plan, problem, main.next, marks, weakest)
    });
    NextPage {
        plan: plan.labeled(content),
        next: main.next,
        progress: main.progress,
        pivots,
    }
}

fn pivots<'a>(
    content: &'a Content,
    plan: &Plan,
    current: &Problem,
    main: Option<NextProblem<'a>>,
    marks: Marks<'_>,
    weakest: Option<&str>,
) -> Vec<Pivot<'a>> {
    let difficulty = plan.filter.difficulty;
    let topics = current
        .topic_set
        .iter()
        .map(|t| (PivotKind::Topic, plan.with_filter(Some(t), difficulty)));
    let others = [
        Some((PivotKind::List, plan.with_filter(None, difficulty))),
        harder(current.difficulty).map(|d| {
            (
                PivotKind::Harder,
                plan.with_filter(plan.filter.topic, Some(d)),
            )
        }),
        weakest
            .and_then(|w| content.topic_id(w))
            .map(|t| (PivotKind::Weakest, plan.with_filter(Some(t), difficulty))),
    ];
    let mut seen = vec![*plan];
    let mut offer = |(kind, candidate): (PivotKind, Plan)| {
        if seen.contains(&candidate) {
            return None;
        }
        seen.push(candidate);
        let next = walk(content, &candidate, Some(&current.slug), marks).next?;
        (main.is_none_or(|m| m.slug != next.slug)).then(|| Pivot {
            kind,
            plan: candidate.labeled(content),
            next,
        })
    };
    // The list, harder and weakest pivots first take their room; the topics fill the rest
    // and are listed first.
    let others: Vec<Pivot<'a>> = others
        .into_iter()
        .flatten()
        .filter_map(&mut offer)
        .collect();
    let room = MAX_PIVOTS.saturating_sub(others.len());
    let mut result: Vec<Pivot<'a>> = topics.filter_map(&mut offer).take(room).collect();
    result.extend(others);
    result.truncate(MAX_PIVOTS);
    result
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;
    use crate::coding::log_of;
    use crate::model::fixtures::{GOOGLE, companies, problem};

    /// Google 6 months, in rank order: p1 Easy [Graph], p2 Hard [Graph, Array],
    /// p3 Medium [Array], p4 Easy [Tree], p5 Medium [Graph].
    fn content() -> Content {
        let tagged = |rank, difficulty, topics: &[&str]| {
            let mut p = problem(rank);
            p.difficulty = difficulty;
            p.topics = topics.iter().map(|t| (*t).to_owned()).collect();
            p
        };
        // Numbered against rank, so number order differs from list order.
        let mut problems = vec![
            tagged(1, Difficulty::Easy, &["Graph"]),
            tagged(2, Difficulty::Hard, &["Graph", "Array"]),
            tagged(3, Difficulty::Medium, &["Array"]),
            tagged(4, Difficulty::Easy, &["Tree"]),
            tagged(5, Difficulty::Medium, &["Graph"]),
        ];
        for (p, id) in problems.iter_mut().zip([50, 40, 30, 20, 10]) {
            p.id = id;
        }
        Content::new(companies(), problems, HashMap::new())
    }

    fn plan(content: &Content, order: PlanOrder) -> Plan {
        Plan {
            list: content.list_id(Some("google"), Some("6m")),
            filter: ProblemFilter::default(),
            status: PlanStatus::Unsolved,
            order,
        }
    }

    fn slugs(content: &Content, plan: &Plan) -> Vec<String> {
        plan.entries(content)
            .iter()
            .map(|e| content.problem_at(e).slug.clone())
            .collect()
    }

    #[test]
    fn orders_by_rank_number_difficulty_and_a_stable_shuffle() {
        let content = content();
        let order = |o| slugs(&content, &plan(&content, o));
        assert_eq!(order(PlanOrder::Rank), ["p1", "p2", "p3", "p4", "p5"]);
        assert_eq!(order(PlanOrder::Number), ["p5", "p4", "p3", "p2", "p1"]);
        assert_eq!(order(PlanOrder::EasyFirst), ["p1", "p4", "p3", "p5", "p2"]);
        let shuffled = order(PlanOrder::Random);
        assert_eq!(shuffled, order(PlanOrder::Random), "the same every time");
        let mut sorted = shuffled.clone();
        sorted.sort();
        assert_eq!(sorted, order(PlanOrder::Rank));
        // The status is not part of the seed; the filter is.
        let untried = Plan {
            status: PlanStatus::Untried,
            ..plan(&content, PlanOrder::Random)
        };
        assert_eq!(slugs(&content, &untried), shuffled);
    }

    #[test]
    fn walks_to_the_next_problem_that_still_counts_and_wraps() {
        let content = content();
        let log = log_of(&["p2", "p3"], &["p4"]);
        let marks = &log;
        let next = |status, after| {
            let plan = Plan {
                status,
                ..plan(&content, PlanOrder::Rank)
            };
            walk(&content, &plan, after, marks).next.map(|n| n.slug)
        };
        assert_eq!(next(PlanStatus::Unsolved, None), Some("p1"));
        assert_eq!(next(PlanStatus::Unsolved, Some("p1")), Some("p4"));
        assert_eq!(next(PlanStatus::Untried, Some("p1")), Some("p5"));
        assert_eq!(next(PlanStatus::All, Some("p1")), Some("p2"));
        // Wraps to the start, never offering the current problem.
        assert_eq!(next(PlanStatus::Unsolved, Some("p5")), Some("p1"));
        assert_eq!(next(PlanStatus::All, Some("p5")), Some("p1"));
        // A problem outside the plan starts it from the top.
        assert_eq!(next(PlanStatus::Untried, Some("nope")), Some("p1"));

        let progress = walk(&content, &plan(&content, PlanOrder::Rank), None, marks).progress;
        assert_eq!(
            progress,
            PlanProgress {
                solved: 2,
                total: 5
            }
        );
    }

    #[test]
    fn a_shaky_plan_walks_the_solves_that_needed_failures() {
        use openleet_proto::Verdict::{Accepted, CompileError, TimeLimitExceeded, WrongAnswer};
        let content = content();
        let mut log = CodingLog::default();
        for (slug, verdict) in [
            ("p1", Accepted),
            ("p2", TimeLimitExceeded),
            ("p2", Accepted),
            ("p4", CompileError),
            ("p4", CompileError),
            ("p4", Accepted),
            ("p5", WrongAnswer),
            ("p5", WrongAnswer),
        ] {
            log.record(slug, 0, verdict);
        }
        let shaky = Plan {
            status: PlanStatus::Shaky,
            ..plan(&content, PlanOrder::Rank)
        };
        assert_eq!(shaky.label(&content), "Google · 6 months · Shaky solves");
        let walked = walk(&content, &shaky, None, &log);
        assert_eq!(walked.next.map(|n| n.slug), Some("p2"));
        // p2 is the only one: from it, nothing else to offer.
        assert_eq!(walk(&content, &shaky, Some("p2"), &log).next, None);
        assert_eq!("shaky".parse(), Ok(PlanStatus::Shaky));
    }

    #[test]
    fn an_exhausted_plan_has_no_next_problem() {
        let content = content();
        let log = log_of(&["p1", "p2", "p3", "p4", "p5"], &[]);
        let marks = &log;
        let plan = plan(&content, PlanOrder::Rank);
        let walked = walk(&content, &plan, Some("p3"), marks);
        assert_eq!(walked.next, None);
        assert_eq!(walked.progress.solved, 5);
        // Only the current problem left: still nothing to offer.
        let almost = log_of(&["p1", "p2", "p4", "p5"], &[]);
        let marks = &almost;
        assert_eq!(walk(&content, &plan, Some("p3"), marks).next, None);
        let page = next_page(&content, &plan, content.problem("p3"), marks, None);
        assert_eq!((page.next, page.progress.total), (None, 5));
    }

    #[test]
    fn labels_plans_without_their_defaults() {
        let content = content();
        let mut plan = plan(&content, PlanOrder::Rank);
        assert_eq!(plan.label(&content), "Google · 6 months · Unsolved");
        plan.filter = content.problem_filter(Some("Graph"), Some("Hard"));
        plan.status = PlanStatus::All;
        plan.order = PlanOrder::EasyFirst;
        assert_eq!(
            plan.label(&content),
            "Google · 6 months · Graph · Hard · Easy first"
        );
        plan.list = content.list_id(Some("meta"), Some("lc1000"));
        assert_eq!(
            plan.label(&content),
            "LC 1–1000 · Graph · Hard · Easy first"
        );
        let view = serde_json::to_value(plan.labeled(&content)).expect("json");
        assert_eq!(
            view,
            serde_json::json!({"company": "meta", "period": "lc1000", "topic": "Graph",
                "difficulty": "Hard", "status": "all", "order": "easy-first",
                "label": "LC 1–1000 · Graph · Hard · Easy first"})
        );
        let next = serde_json::to_value(walk(&content, &plan, None, &CodingLog::default()).next)
            .expect("json");
        assert!(next.get("topics").is_none(), "{next}");
    }

    #[test]
    fn pivots_from_the_solved_problem_without_repeats() {
        let content = content();
        let log = log_of(&["p2"], &[]);
        let marks = &log;
        let graph = Plan {
            filter: content.problem_filter(Some("Graph"), None),
            ..plan(&content, PlanOrder::Rank)
        };
        let page = next_page(&content, &graph, content.problem("p2"), marks, Some("Tree"));
        assert_eq!(page.next.map(|n| n.slug), Some("p5"));
        let pivots: Vec<_> = page
            .pivots
            .iter()
            .map(|p| (p.kind, p.plan.topic, p.plan.difficulty, p.next.slug))
            .collect();
        // Graph is the plan itself, so of p2's topics only Array is offered; the whole list
        // goes on to p3; nothing is harder than Hard; the weakest topic is Tree.
        assert_eq!(
            pivots,
            [
                (PivotKind::Topic, Some("Array"), None, "p3"),
                (PivotKind::List, None, None, "p3"),
                (PivotKind::Weakest, Some("Tree"), None, "p4"),
            ]
        );
        assert!(pivots.len() <= MAX_PIVOTS);
        assert!(page.pivots.iter().all(|p| p.kind != PivotKind::Harder));

        // A pivot whose next is the plan's own next is left out: from p1 the Medium problems
        // start at p3, the plan's next anyway.
        let rank = plan(&content, PlanOrder::Rank);
        let kinds = |slug| {
            let page = next_page(&content, &rank, content.problem(slug), marks, None);
            let pivots: Vec<_> = page
                .pivots
                .iter()
                .map(|p| (p.kind, p.plan.difficulty, p.next.slug))
                .collect();
            (page.next.map(|n| n.slug), pivots)
        };
        assert_eq!(
            kinds("p1"),
            (Some("p3"), vec![(PivotKind::Topic, None, "p5")])
        );
        // From Easy p4 the harder pivot is Medium.
        assert_eq!(
            kinds("p4"),
            (
                Some("p5"),
                vec![(PivotKind::Harder, Some(Difficulty::Medium), "p3")]
            )
        );
        // No current problem, no pivots.
        assert!(
            next_page(&content, &rank, None, marks, None)
                .pivots
                .is_empty()
        );
    }

    #[test]
    fn fills_at_most_four_pivots_trimming_the_topics() {
        // Google 6 months, all Easy but p6: p1 [A, B, C], p2 [Z], p3 [A], p4 [B], p5 [C],
        // p6 Medium [A], p7 [W].
        let tagged = |rank, difficulty, topics: &[&str]| {
            let mut p = problem(rank);
            p.difficulty = difficulty;
            p.topics = topics.iter().map(|t| (*t).to_owned()).collect();
            p
        };
        let easy = Difficulty::Easy;
        let content = Content::new(
            companies(),
            vec![
                tagged(1, easy, &["A", "B", "C"]),
                tagged(2, easy, &["Z"]),
                tagged(3, easy, &["A"]),
                tagged(4, easy, &["B"]),
                tagged(5, easy, &["C"]),
                tagged(6, Difficulty::Medium, &["A"]),
                tagged(7, easy, &["W"]),
            ],
            HashMap::new(),
        );
        let none = CodingLog::default();
        let marks = &none;
        let a = Plan {
            filter: content.problem_filter(Some("A"), None),
            ..plan(&content, PlanOrder::Rank)
        };
        let page = next_page(&content, &a, content.problem("p1"), marks, Some("W"));
        assert_eq!(page.next.map(|n| n.slug), Some("p3"));
        let pivots: Vec<_> = page
            .pivots
            .iter()
            .map(|p| (p.kind, p.plan.topic, p.next.slug))
            .collect();
        // Three pivots of other kinds leave room for one topic: B, not C.
        assert_eq!(
            pivots,
            [
                (PivotKind::Topic, Some("B"), "p4"),
                (PivotKind::List, None, "p2"),
                (PivotKind::Harder, Some("A"), "p6"),
                (PivotKind::Weakest, Some("W"), "p7"),
            ]
        );
        assert_eq!(content.companies.get(GOOGLE).slug, "google");
    }
}
