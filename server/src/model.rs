//! Shared domain types: problems, approaches, grades and attempts (port of `web/src/lib/types.ts`).

use serde::{Deserialize, Serialize};

/// Error returned when a query value names no known variant.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
#[error("unknown {kind}: {value}")]
pub struct ParseEnumError {
    /// What was being parsed, such as "period".
    pub kind: &'static str,
    /// The rejected input.
    pub value: String,
}

/// Defines a fieldless enum whose wire form is a fixed string, with `as_str`, `ALL`,
/// `Display` and `FromStr` derived from one table so the spellings live in one place.
macro_rules! wire_enum {
    (
        $(#[$meta:meta])*
        $name:ident: $kind:literal { $($(#[$vmeta:meta])* $variant:ident = $wire:literal),+ $(,)? }
    ) => {
        $(#[$meta])*
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, ::serde::Serialize, ::serde::Deserialize)]
        pub enum $name {
            $($(#[$vmeta])* #[serde(rename = $wire)] $variant),+
        }

        impl $name {
            /// Every variant, in declaration order.
            pub const ALL: &[Self] = &[$(Self::$variant),+];

            /// The wire spelling used in JSON and query strings.
            #[must_use]
            pub const fn as_str(self) -> &'static str {
                match self {
                    $(Self::$variant => $wire),+
                }
            }
        }

        impl ::std::fmt::Display for $name {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                f.write_str(self.as_str())
            }
        }

        impl ::std::str::FromStr for $name {
            type Err = $crate::model::ParseEnumError;

            fn from_str(value: &str) -> Result<Self, Self::Err> {
                match value {
                    $($wire => Ok(Self::$variant),)+
                    _ => Err($crate::model::ParseEnumError { kind: $kind, value: value.to_owned() }),
                }
            }
        }
    };
}
pub(crate) use wire_enum;

wire_enum! {
    /// LeetCode difficulty.
    Difficulty: "difficulty" { Easy = "Easy", Medium = "Medium", Hard = "Hard" }
}

wire_enum! {
    /// Which problem list to study: a Google frequency window, or LeetCode 1 to 1000.
    #[derive(Default)]
    Period: "period" {
        /// Asked by Google in the last 30 days.
        Days30 = "30d",
        /// Asked by Google in the last 3 months.
        Months3 = "3m",
        /// Asked by Google in the last 6 months (the default list).
        #[default]
        Months6 = "6m",
        /// Free LeetCode problems numbered 1 to 1000, Google or not.
        Lc1000 = "lc1000",
    }
}

impl Period {
    /// Label shown in the UI.
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Days30 => "30 days",
            Self::Months3 => "3 months",
            Self::Months6 => "6 months",
            Self::Lc1000 => "LC 1–1000",
        }
    }
}

wire_enum! {
    /// What the learner did with a card. "again" adds it to the visit-again list, "less" to the
    /// visit-less-often list, "good" clears both, and "skip" defers it without a grade.
    Grade: "grade" { Again = "again", Good = "good", Less = "less", Skip = "skip" }
}

/// Highest problem number in the "LC 1–1000" list.
pub const LC_LIMIT: u32 = 1000;
/// Rank given to problems Google did not ask, so they sort after every Google problem.
pub const UNRANKED_BASE: u32 = 100_000;

/// Position and frequency (0-100) of a problem in one period's list.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Asked {
    /// 1-based position in the period's list.
    pub rank: u32,
    /// How often Google asked it, 0-100.
    pub frequency: f64,
}

/// Google frequency per period. Each list is a subset of the next; classic-only problems
/// have none. Serializes back to the same object, keyed by "30d" / "3m" / "6m".
#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize)]
pub struct AskedBy {
    /// The 30-day list entry.
    #[serde(rename = "30d", default, skip_serializing_if = "Option::is_none")]
    pub days30: Option<Asked>,
    /// The 3-month list entry.
    #[serde(rename = "3m", default, skip_serializing_if = "Option::is_none")]
    pub months3: Option<Asked>,
    /// The 6-month list entry; absent for classic-only problems.
    #[serde(rename = "6m", default, skip_serializing_if = "Option::is_none")]
    pub months6: Option<Asked>,
}

impl AskedBy {
    /// The entry for a Google period; always `None` for [`Period::Lc1000`].
    #[must_use]
    pub const fn get(&self, period: Period) -> Option<&Asked> {
        match period {
            Period::Days30 => self.days30.as_ref(),
            Period::Months3 => self.months3.as_ref(),
            Period::Months6 => self.months6.as_ref(),
            Period::Lc1000 => None,
        }
    }
}

/// One row of `data/problems.json` (built by `uv run google ingest`).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Problem {
    /// LeetCode problem number.
    pub id: u32,
    /// LeetCode slug, unique.
    pub slug: String,
    /// Display title.
    pub title: String,
    /// LeetCode difficulty.
    pub difficulty: Difficulty,
    /// Google frequency per period; empty for classic-only problems.
    pub asked: AskedBy,
    /// Link to the problem on LeetCode.
    pub url: String,
    /// LeetCode topic tags.
    pub topics: Vec<String>,
    /// Whether the problem needs LeetCode Premium.
    pub premium: bool,
    /// Sanitized HTML statement; `None` for premium problems.
    pub description: Option<String>,
}

impl Problem {
    /// Whether Google asked this problem in the last 6 months (it counts toward readiness).
    #[must_use]
    pub const fn is_google(&self) -> bool {
        self.asked.months6.is_some()
    }

    /// The 6-month Google rank, or `100000 + id` for classic-only problems.
    #[must_use]
    pub fn rank(&self) -> u32 {
        self.asked
            .months6
            .map_or(UNRANKED_BASE + self.id, |asked| asked.rank)
    }

    /// The 6-month Google frequency, or 0 for classic-only problems.
    #[must_use]
    pub fn frequency(&self) -> f64 {
        self.asked.months6.map_or(0.0, |asked| asked.frequency)
    }

    /// Whether the problem belongs to a period's list.
    #[must_use]
    pub const fn in_period(&self, period: Period) -> bool {
        match period {
            Period::Lc1000 => self.id <= LC_LIMIT && !self.premium,
            _ => self.asked.get(period).is_some(),
        }
    }

    /// Order of an unseen card in a period's list: the period's Google rank (falling back to
    /// [`Problem::rank`]), or the problem number for "LC 1–1000".
    #[must_use]
    pub fn new_card_rank(&self, period: Period) -> u32 {
        match period {
            Period::Lc1000 => self.id,
            _ => self
                .asked
                .get(period)
                .map_or_else(|| self.rank(), |a| a.rank),
        }
    }

    /// Whether the problem carries this topic tag.
    #[must_use]
    pub fn has_topic(&self, topic: &str) -> bool {
        self.topics.iter().any(|t| t == topic)
    }
}

/// One entry of `data/approaches.json`, written in ASD-STE100 Simplified Technical English.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Approach {
    /// The key idea in one sentence.
    pub insight: String,
    /// The algorithm, one step per entry.
    pub steps: Vec<String>,
    /// Time complexity.
    pub time: String,
    /// Space complexity.
    pub space: String,
    /// Nudges shown one at a time before the answer; they never name the technique.
    #[serde(default)]
    pub hints: Vec<String>,
}

/// One answer in the attempt log.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Attempt {
    /// The problem answered.
    pub slug: String,
    /// When, in Unix milliseconds.
    pub at: i64,
    /// The learner's grade.
    pub grade: Grade,
    /// Topics the learner guessed.
    pub guessed: Vec<String>,
    /// Topic-guess F1 in [0, 1]; `None` for skips.
    pub score: Option<f64>,
    /// How many hints the learner opened before answering.
    pub hints: u32,
}

#[cfg(test)]
pub(crate) mod fixtures {
    //! Builders shared by the unit tests (port of `web/src/lib/test-fixtures.ts`).

    use super::{Asked, AskedBy, Attempt, Difficulty, Grade, Problem};

    /// 2026-01-01T00:00:00Z in milliseconds.
    pub const T0: i64 = 1_767_225_600_000;

    /// A Medium "Array" problem numbered and ranked `rank`, asked with frequency 10.
    pub fn problem(rank: u32) -> Problem {
        Problem {
            id: rank,
            slug: format!("p{rank}"),
            title: format!("Problem {rank}"),
            difficulty: Difficulty::Medium,
            asked: AskedBy {
                months6: Some(Asked {
                    rank,
                    frequency: 10.0,
                }),
                ..AskedBy::default()
            },
            url: String::new(),
            topics: vec!["Array".to_owned()],
            premium: false,
            description: None,
        }
    }

    /// An attempt at `at` with score 1 (or none for a skip).
    pub fn attempt(slug: &str, grade: Grade, at: i64) -> Attempt {
        let score = (grade != Grade::Skip).then_some(1.0);
        attempt_scored(slug, grade, at, score)
    }

    /// An attempt with an explicit score.
    pub fn attempt_scored(slug: &str, grade: Grade, at: i64, score: Option<f64>) -> Attempt {
        Attempt {
            slug: slug.to_owned(),
            at,
            grade,
            guessed: Vec::new(),
            score,
            hints: 0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn asked_round_trips_including_empty() {
        let json = r#"{"30d":{"rank":1,"frequency":100.0},"6m":{"rank":3,"frequency":9.5}}"#;
        let asked: AskedBy = serde_json::from_str(json).expect("parse");
        assert_eq!(serde_json::to_string(&asked).expect("serialize"), json);
        let empty: AskedBy = serde_json::from_str("{}").expect("parse");
        assert_eq!(serde_json::to_string(&empty).expect("serialize"), "{}");
        assert_eq!(empty.get(Period::Months6), None);
    }

    #[test]
    fn periods_parse_and_label() {
        assert_eq!("lc1000".parse::<Period>(), Ok(Period::Lc1000));
        assert_eq!(Period::Lc1000.label(), "LC 1–1000");
        assert!("1y".parse::<Period>().is_err());
        assert_eq!(Period::default(), Period::Months6);
        assert_eq!(
            serde_json::to_string(&Period::Days30).expect("serialize"),
            r#""30d""#
        );
    }

    #[test]
    fn classic_problems_fall_back() {
        let mut p = fixtures::problem(7);
        p.asked = AskedBy::default();
        assert_eq!(p.rank(), 100_007);
        assert!(p.frequency().abs() < f64::EPSILON);
        assert!(!p.is_google());
        assert!(p.in_period(Period::Lc1000));
        assert!(!p.in_period(Period::Months6));
        assert_eq!(p.new_card_rank(Period::Months6), 100_007);
        p.premium = true;
        assert!(!p.in_period(Period::Lc1000));
        let mut big = fixtures::problem(1001);
        big.asked = AskedBy::default();
        assert!(!big.in_period(Period::Lc1000));
    }
}
