//! Shared domain types: companies, problems, approaches, grades and attempts.

use std::collections::HashMap;
use std::num::NonZeroU16;

use serde::ser::SerializeMap;
use serde::{Deserialize, Serialize, Serializer};

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
    /// Which list to study: a company's frequency window, or LeetCode 1 to 1000.
    #[derive(Default)]
    Period: "period" {
        /// Asked in the last 30 days.
        Days30 = "30d",
        /// Asked in the last 3 months.
        Months3 = "3m",
        /// Asked in the last 6 months (the default list).
        #[default]
        Months6 = "6m",
        /// Asked at any time.
        All = "all",
        /// Free LeetCode problems numbered 1 to 1000, whoever asked them.
        Lc1000 = "lc1000",
    }
}

impl Period {
    /// The periods companies list problems for, in [`Periods`] slot order.
    pub const COMPANY: [Self; PERIOD_SLOTS] =
        [Self::Days30, Self::Months3, Self::Months6, Self::All];

    /// Label shown in the UI.
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Days30 => "30 days",
            Self::Months3 => "3 months",
            Self::Months6 => "6 months",
            Self::All => "All time",
            Self::Lc1000 => "LC 1–1000",
        }
    }

    /// Index into [`Periods`]; `None` for [`Period::Lc1000`], which no company lists.
    #[must_use]
    pub const fn slot(self) -> Option<usize> {
        match self {
            Self::Days30 => Some(0),
            Self::Months3 => Some(1),
            Self::Months6 => Some(2),
            Self::All => Some(3),
            Self::Lc1000 => None,
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
/// Rank given to problems no company asked in 6 months, so they sort after every asked one.
pub const UNRANKED_BASE: u32 = 100_000;
/// How many periods a company lists problems for.
pub const PERIOD_SLOTS: usize = 4;

/// Position and frequency (0-100) of a problem in one company's list for one period.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Asked {
    /// 1-based position in the list.
    pub rank: NonZeroU16,
    /// How often the company asked it, 0-100.
    pub frequency: f32,
}

impl Asked {
    /// The rank as a plain number.
    #[must_use]
    pub fn position(self) -> u32 {
        u32::from(self.rank.get())
    }
}

/// One company's entries per period, indexed by [`Period::slot`].
pub type Periods = [Option<Asked>; PERIOD_SLOTS];

/// Index of a company in the [`Companies`] table (picker order).
pub type CompanyId = u8;

/// One company's lists for a problem.
#[derive(Debug, Clone, PartialEq)]
pub struct CompanyAsked {
    /// The company.
    pub company: CompanyId,
    /// Its entries per period.
    pub periods: Periods,
}

/// A company of the picker.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Company {
    /// URL-safe identifier, such as "google".
    pub slug: String,
    /// Display name.
    pub name: String,
    /// Problems it asked in any period.
    pub problems: u32,
}

/// More companies than a [`CompanyId`] can name.
#[derive(Debug, Clone, Copy, PartialEq, Eq, thiserror::Error)]
#[error("at most 255 companies are supported")]
pub struct TooManyCompanies;

/// The companies in picker order, interned to small ids.
#[derive(Debug, Clone, Default)]
pub struct Companies {
    list: Vec<Company>,
    by_slug: HashMap<String, CompanyId>,
}

impl Companies {
    /// Interns the companies in the given (picker) order. A repeated slug keeps its first id.
    ///
    /// # Errors
    /// When there are more than 255 companies.
    pub fn new(list: Vec<Company>) -> Result<Self, TooManyCompanies> {
        let mut companies = Self::default();
        for company in list {
            companies.push(company)?;
        }
        Ok(companies)
    }

    fn push(&mut self, company: Company) -> Result<CompanyId, TooManyCompanies> {
        if let Some(&id) = self.by_slug.get(&company.slug) {
            return Ok(id);
        }
        let id = CompanyId::try_from(self.list.len()).map_err(|_| TooManyCompanies)?;
        if id == CompanyId::MAX {
            return Err(TooManyCompanies);
        }
        self.by_slug.insert(company.slug.clone(), id);
        self.list.push(company);
        Ok(id)
    }

    /// The id of `slug`, adding an unlisted company (named after its slug) at the end.
    ///
    /// # Errors
    /// When the table is full.
    pub fn intern(&mut self, slug: &str) -> Result<CompanyId, TooManyCompanies> {
        match self.by_slug.get(slug) {
            Some(&id) => Ok(id),
            None => self.push(Company {
                slug: slug.to_owned(),
                name: slug.to_owned(),
                problems: 0,
            }),
        }
    }

    /// The id of a company slug.
    #[must_use]
    pub fn id(&self, slug: &str) -> Option<CompanyId> {
        self.by_slug.get(slug).copied()
    }

    /// The company with this id; ids come from this table, so it always exists.
    #[must_use]
    pub fn get(&self, id: CompanyId) -> &Company {
        &self.list[usize::from(id)]
    }

    /// Every company, in picker order.
    #[must_use]
    pub fn as_slice(&self) -> &[Company] {
        &self.list
    }

    /// Number of companies.
    #[must_use]
    pub const fn len(&self) -> usize {
        self.list.len()
    }

    /// Whether the table is empty.
    #[must_use]
    pub const fn is_empty(&self) -> bool {
        self.list.is_empty()
    }

    pub(crate) fn set_count(&mut self, id: CompanyId, problems: u32) {
        self.list[usize::from(id)].problems = problems;
    }
}

/// Index of a topic in the content's topic table, most common first.
pub type TopicId = u8;
/// Most distinct topics a [`TopicSet`] holds.
pub const MAX_TOPICS: usize = 256;

/// A problem's topics as a fixed 256-bit set over [`TopicId`]s: a membership test is one
/// shift and mask, with no string compare and no allocation.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Hash)]
pub struct TopicSet([u64; MAX_TOPICS / 64]);

impl TopicSet {
    /// Adds a topic.
    pub const fn insert(&mut self, id: TopicId) {
        self.0[(id >> 6) as usize] |= 1 << (id & 63);
    }

    /// Whether the set holds this topic.
    #[must_use]
    pub const fn contains(self, id: TopicId) -> bool {
        self.0[(id >> 6) as usize] & (1 << (id & 63)) != 0
    }

    /// Every topic in the set, lowest id (most common topic) first.
    pub fn iter(self) -> impl Iterator<Item = TopicId> {
        (0_u8..).zip(self.0).flat_map(|(word, mut bits)| {
            std::iter::from_fn(move || {
                if bits == 0 {
                    return None;
                }
                #[allow(
                    clippy::cast_possible_truncation,
                    reason = "a u64 has fewer than 64 trailing zeros once it is not 0"
                )]
                let bit = bits.trailing_zeros() as u8;
                bits &= bits - 1;
                Some(word * 64 + bit)
            })
        })
    }
}

/// Whose lists to use: one company's, or every company's ("any").
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum CompanyFilter {
    /// Asked by at least one company.
    Any,
    /// Asked by this company.
    Company(CompanyId),
}

/// One problem of the content, compact: company lists are interned and sorted by company.
#[derive(Debug, Clone, PartialEq)]
pub struct Problem {
    /// LeetCode problem number.
    pub id: u32,
    /// LeetCode slug, unique.
    pub slug: String,
    /// Display title.
    pub title: String,
    /// LeetCode difficulty.
    pub difficulty: Difficulty,
    /// Every company that lists it, in picker order; empty for classic-only problems.
    pub companies: Box<[CompanyAsked]>,
    /// Link to the problem on LeetCode.
    pub url: String,
    /// LeetCode topic tags.
    pub topics: Vec<String>,
    /// The same tags as ids of the content's topic table, for filtering; filled in by
    /// [`crate::content::Content::new`].
    pub topic_set: TopicSet,
    /// Whether the problem needs LeetCode Premium.
    pub premium: bool,
    /// Sanitized HTML statement; `None` only when no source has one.
    pub description: Option<String>,
}

impl Problem {
    /// A company's entry for a period.
    #[must_use]
    pub fn asked(&self, company: CompanyId, period: Period) -> Option<Asked> {
        let slot = period.slot()?;
        self.companies
            .iter()
            .find(|c| c.company == company)
            .and_then(|c| c.periods[slot])
    }

    /// Every company entry for a period.
    pub fn asked_in(&self, period: Period) -> impl Iterator<Item = Asked> + '_ {
        let slot = period.slot();
        self.companies
            .iter()
            .filter_map(move |c| slot.and_then(|s| c.periods[s]))
    }

    /// The highest frequency any company gives it in a period.
    #[must_use]
    pub fn best_frequency(&self, period: Period) -> Option<f32> {
        self.asked_in(period).map(|a| a.frequency).reduce(f32::max)
    }

    /// The best 6-month rank across companies, or `100000 + id` when no company asked it in
    /// 6 months.
    #[must_use]
    pub fn rank(&self) -> u32 {
        self.asked_in(Period::Months6)
            .map(Asked::position)
            .min()
            .unwrap_or(UNRANKED_BASE + self.id)
    }

    /// Whether the problem is in "LC 1–1000".
    #[must_use]
    pub const fn in_lc1000(&self) -> bool {
        self.id <= LC_LIMIT
    }

    /// Whether the problem carries this topic tag.
    #[must_use]
    pub fn has_topic(&self, topic: &str) -> bool {
        self.topics.iter().any(|t| t == topic)
    }

    /// Whether the problem carries this topic, by id; one bit test.
    #[must_use]
    pub const fn has_topic_id(&self, topic: TopicId) -> bool {
        self.topic_set.contains(topic)
    }

    /// The problem as JSON, with company ids resolved through `companies`.
    #[must_use]
    pub fn view<'a>(&'a self, companies: &'a Companies) -> ProblemView<'a> {
        ProblemView {
            id: self.id,
            slug: &self.slug,
            title: &self.title,
            difficulty: self.difficulty,
            companies: CompaniesJson {
                asked: &self.companies,
                table: companies,
            },
            url: &self.url,
            topics: &self.topics,
            premium: self.premium,
            description: self.description.as_deref(),
        }
    }

    /// Slugs of every company that lists it, in picker order, as a JSON array.
    #[must_use]
    pub fn company_slugs<'a>(&'a self, companies: &'a Companies) -> CompanySlugs<'a> {
        CompanySlugs {
            asked: &self.companies,
            table: companies,
        }
    }
}

/// A problem in the JSON shape of `problems.json`, borrowing everything.
#[derive(Debug, Clone, Serialize)]
pub struct ProblemView<'a> {
    /// LeetCode problem number.
    pub id: u32,
    /// Slug.
    pub slug: &'a str,
    /// Title.
    pub title: &'a str,
    /// Difficulty.
    pub difficulty: Difficulty,
    /// `{"google": {"30d": {"rank", "frequency"}, ...}, ...}`.
    pub companies: CompaniesJson<'a>,
    /// LeetCode link.
    pub url: &'a str,
    /// Topic tags.
    pub topics: &'a [String],
    /// Premium only.
    pub premium: bool,
    /// HTML statement.
    pub description: Option<&'a str>,
}

impl PartialEq for ProblemView<'_> {
    fn eq(&self, other: &Self) -> bool {
        self.slug == other.slug
    }
}

/// A problem's company lists as a JSON object keyed by company slug, then by period.
#[derive(Debug, Clone, Copy)]
pub struct CompaniesJson<'a> {
    asked: &'a [CompanyAsked],
    table: &'a Companies,
}

struct PeriodsJson<'a>(&'a Periods);

impl Serialize for PeriodsJson<'_> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        let mut map = serializer.serialize_map(Some(self.0.iter().flatten().count()))?;
        for (period, asked) in Period::COMPANY.iter().zip(self.0) {
            if let Some(asked) = asked {
                map.serialize_entry(period.as_str(), asked)?;
            }
        }
        map.end()
    }
}

impl Serialize for CompaniesJson<'_> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        let mut map = serializer.serialize_map(Some(self.asked.len()))?;
        for entry in self.asked {
            map.serialize_entry(
                &self.table.get(entry.company).slug,
                &PeriodsJson(&entry.periods),
            )?;
        }
        map.end()
    }
}

/// Company slugs of a problem as a JSON array.
#[derive(Debug, Clone, Copy)]
pub struct CompanySlugs<'a> {
    asked: &'a [CompanyAsked],
    table: &'a Companies,
}

impl PartialEq for CompanySlugs<'_> {
    fn eq(&self, other: &Self) -> bool {
        self.asked == other.asked
    }
}

impl Serialize for CompanySlugs<'_> {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serializer.collect_seq(
            self.asked
                .iter()
                .filter(|c| c.periods.iter().any(Option::is_some))
                .map(|c| self.table.get(c.company).slug.as_str()),
        )
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
    //! Builders shared by the unit tests.

    use std::num::NonZeroU16;

    use super::{
        Asked, Attempt, Companies, Company, CompanyAsked, CompanyId, Difficulty, Grade, Period,
        Problem,
    };

    /// 2026-01-01T00:00:00Z in milliseconds.
    pub const T0: i64 = 1_767_225_600_000;
    /// Company 0 of [`companies`].
    pub const GOOGLE: CompanyId = 0;
    /// Company 1 of [`companies`].
    pub const META: CompanyId = 1;

    /// Google and Meta.
    pub fn companies() -> Companies {
        let company = |slug: &str, name: &str| Company {
            slug: slug.to_owned(),
            name: name.to_owned(),
            problems: 0,
        };
        Companies::new(vec![company("google", "Google"), company("meta", "Meta")])
            .expect("two companies")
    }

    /// An entry with this rank and frequency.
    pub fn asked(rank: u16, frequency: f32) -> Asked {
        Asked {
            rank: NonZeroU16::new(rank).expect("rank above 0"),
            frequency,
        }
    }

    /// A Medium "Array" problem numbered `id`, asked by no company.
    pub fn classic(id: u32) -> Problem {
        Problem {
            id,
            slug: format!("p{id}"),
            title: format!("Problem {id}"),
            difficulty: Difficulty::Medium,
            companies: Box::new([]),
            url: String::new(),
            topics: vec!["Array".to_owned()],
            topic_set: super::TopicSet::default(),
            premium: false,
            description: None,
        }
    }

    /// Lists a problem for a company in a period.
    pub fn with(mut problem: Problem, company: CompanyId, period: Period, entry: Asked) -> Problem {
        let slot = period.slot().expect("a company period");
        let mut list = problem.companies.into_vec();
        if let Some(c) = list.iter_mut().find(|c| c.company == company) {
            c.periods[slot] = Some(entry);
        } else {
            let mut periods = [None; super::PERIOD_SLOTS];
            periods[slot] = Some(entry);
            list.push(CompanyAsked { company, periods });
            list.sort_by_key(|c| c.company);
        }
        problem.companies = list.into_boxed_slice();
        problem
    }

    /// A problem numbered `rank` and ranked `rank` by company 0 over 6 months, frequency 10.
    pub fn problem(rank: u16) -> Problem {
        with(
            classic(u32::from(rank)),
            GOOGLE,
            Period::Months6,
            asked(rank, 10.0),
        )
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
    use super::fixtures::{GOOGLE, META, asked, classic, companies, problem, with};
    use super::*;

    #[test]
    fn serializes_company_lists_like_the_data_file() {
        let p = with(problem(3), META, Period::All, asked(7, 9.5));
        let p = with(p, GOOGLE, Period::Days30, asked(1, 100.0));
        let table = companies();
        let json = serde_json::to_string(&p.view(&table).companies).expect("serialize");
        assert_eq!(
            json,
            r#"{"google":{"30d":{"rank":1,"frequency":100.0},"6m":{"rank":3,"frequency":10.0}},"meta":{"all":{"rank":7,"frequency":9.5}}}"#
        );
        let slugs = serde_json::to_string(&p.company_slugs(&table)).expect("serialize");
        assert_eq!(slugs, r#"["google","meta"]"#);
        let none = classic(9);
        assert_eq!(
            serde_json::to_string(&none.view(&table).companies).expect("serialize"),
            "{}"
        );
    }

    #[test]
    fn periods_parse_and_label() {
        assert_eq!("lc1000".parse::<Period>(), Ok(Period::Lc1000));
        assert_eq!("all".parse::<Period>(), Ok(Period::All));
        assert_eq!(Period::Lc1000.label(), "LC 1–1000");
        assert!("1y".parse::<Period>().is_err());
        assert_eq!(Period::default(), Period::Months6);
        assert_eq!(Period::Lc1000.slot(), None);
    }

    #[test]
    fn ranks_by_the_best_company() {
        let p = with(problem(30), META, Period::Months6, asked(4, 55.0));
        assert_eq!(p.rank(), 4);
        assert_eq!(p.best_frequency(Period::Months6), Some(55.0));
        assert_eq!(p.asked(META, Period::Days30), None);
        assert_eq!(
            p.asked(GOOGLE, Period::Months6).map(Asked::position),
            Some(30)
        );
        let c = classic(7);
        assert_eq!((c.rank(), c.best_frequency(Period::All)), (100_007, None));
        assert!(c.in_lc1000() && !classic(1001).in_lc1000());
    }

    #[test]
    fn topic_sets_hold_every_id_and_list_them_in_order() {
        let mut set = TopicSet::default();
        assert_eq!(set.iter().count(), 0);
        for id in [200, 0, 63, 64, 255, 127] {
            set.insert(id);
        }
        set.insert(64);
        assert_eq!(set.iter().collect::<Vec<_>>(), [0, 63, 64, 127, 200, 255]);
        assert!(set.contains(255) && set.contains(0) && !set.contains(1) && !set.contains(128));
        let mut p = classic(1);
        p.topic_set = set;
        assert!(p.has_topic_id(200) && !p.has_topic_id(201));
    }

    #[test]
    fn interns_companies() {
        let mut table = companies();
        assert_eq!(table.id("meta"), Some(META));
        assert_eq!(table.intern("stripe"), Ok(2));
        assert_eq!(table.get(2).name, "stripe");
        assert_eq!(table.len(), 3);
    }
}
