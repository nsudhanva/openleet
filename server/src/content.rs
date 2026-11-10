//! The read-only study content, loaded once and kept in memory: problems, companies,
//! approaches, the precomputed study lists and the search index.

use std::collections::HashMap;
use std::io::ErrorKind;
use std::path::Path;

use anyhow::Context as _;
use serde::Deserialize;
use serde::de::DeserializeOwned;

use crate::lists::{ListEntry, ListId, Lists};
use crate::model::{
    Approach, Asked, Companies, Company, CompanyAsked, CompanyFilter, Difficulty, PERIOD_SLOTS,
    Problem, ProblemView,
};
use crate::search::{SearchHit, SearchIndex};

/// The company selected when a request names none (or an unknown one).
pub const DEFAULT_COMPANY: &str = "google";
/// The company filter value meaning "asked by at least one company".
pub const ANY_COMPANY: &str = "any";

/// Problems, companies, approaches and everything built from them.
#[derive(Debug, Default)]
pub struct Content {
    /// Every problem, by LeetCode number.
    pub problems: Vec<Problem>,
    /// The companies, in picker order.
    pub companies: Companies,
    /// Worked approach per slug.
    pub approaches: HashMap<String, Approach>,
    /// Every topic, most common first (ties in order of first use).
    pub topics: Vec<String>,
    /// Search index over `problems`.
    pub search_index: SearchIndex,
    /// Study lists per (company, period).
    pub lists: Lists,
    /// `GET /api/companies`, serialized once.
    companies_json: Box<str>,
    /// Position in `problems` per slug.
    by_slug: HashMap<String, usize>,
}

/// The shape of a problems file. `sources` is not needed at run time.
#[derive(Deserialize)]
struct RawFile {
    companies: Vec<Company>,
    problems: Vec<RawProblem>,
}

#[derive(Deserialize)]
struct RawProblem {
    id: u32,
    slug: String,
    title: String,
    difficulty: Difficulty,
    #[serde(default)]
    companies: HashMap<String, RawPeriods>,
    url: String,
    topics: Vec<String>,
    premium: bool,
    description: Option<String>,
}

#[derive(Deserialize)]
struct RawPeriods {
    #[serde(rename = "30d")]
    days30: Option<Asked>,
    #[serde(rename = "3m")]
    months3: Option<Asked>,
    #[serde(rename = "6m")]
    months6: Option<Asked>,
    all: Option<Asked>,
}

impl From<RawPeriods> for [Option<Asked>; PERIOD_SLOTS] {
    fn from(raw: RawPeriods) -> Self {
        [raw.days30, raw.months3, raw.months6, raw.all]
    }
}

/// Parses a JSON file, or returns `None` when it does not exist.
fn read_json<T: DeserializeOwned>(path: &Path) -> anyhow::Result<Option<T>> {
    let bytes = match std::fs::read(path) {
        Ok(bytes) => bytes,
        Err(error) if error.kind() == ErrorKind::NotFound => return Ok(None),
        Err(error) => return Err(error).with_context(|| format!("reading {}", path.display())),
    };
    serde_json::from_slice(&bytes)
        .map(Some)
        .with_context(|| format!("parsing {}", path.display()))
}

/// Interns company slugs and turns raw problems into compact ones.
fn compact(file: RawFile) -> anyhow::Result<(Companies, Vec<Problem>)> {
    let mut companies = Companies::new(file.companies)?;
    let mut problems = Vec::with_capacity(file.problems.len());
    for raw in file.problems {
        let mut asked = Vec::with_capacity(raw.companies.len());
        for (slug, periods) in raw.companies {
            asked.push(CompanyAsked {
                company: companies.intern(&slug)?,
                periods: periods.into(),
            });
        }
        asked.sort_by_key(|c| c.company);
        problems.push(Problem {
            id: raw.id,
            slug: raw.slug,
            title: raw.title,
            difficulty: raw.difficulty,
            companies: asked.into_boxed_slice(),
            url: raw.url,
            topics: raw.topics,
            premium: raw.premium,
            description: raw.description,
        });
    }
    Ok((companies, problems))
}

/// Topics by how many problems carry them, most first; ties keep order of first use.
fn topics_by_count(problems: &[Problem]) -> Vec<String> {
    let mut index: HashMap<&str, usize> = HashMap::new();
    let mut counts: Vec<(&str, usize)> = Vec::new();
    for topic in problems.iter().flat_map(|p| &p.topics) {
        let i = *index.entry(topic).or_insert_with(|| {
            counts.push((topic, 0));
            counts.len() - 1
        });
        counts[i].1 += 1;
    }
    counts.sort_by_key(|&(_, n)| std::cmp::Reverse(n));
    counts
        .into_iter()
        .map(|(topic, _)| topic.to_owned())
        .collect()
}

impl Content {
    /// Loads a problems file (`{"companies": [...], "problems": [...]}`) and an approaches
    /// file. A missing file counts as empty. Companies a problem names but the table does not
    /// are added at the end of the picker, named after their slug.
    ///
    /// # Errors
    /// When a file exists but cannot be read or parsed, or names more than 255 companies.
    pub fn load(problems: &Path, approaches: &Path) -> anyhow::Result<Self> {
        let (companies, problems) = match read_json::<RawFile>(problems)? {
            Some(file) => compact(file)?,
            None => (Companies::default(), Vec::new()),
        };
        let approaches = read_json(approaches)?.unwrap_or_default();
        Ok(Self::new(companies, problems, approaches))
    }

    /// Builds the indexes and lists over parsed content. Company problem counts are
    /// recomputed from the problems.
    #[must_use]
    pub fn new(
        mut companies: Companies,
        problems: Vec<Problem>,
        approaches: HashMap<String, Approach>,
    ) -> Self {
        let mut counts = vec![0_u32; companies.len()];
        for c in problems.iter().flat_map(|p| p.companies.iter()) {
            if c.periods.iter().any(Option::is_some) {
                counts[usize::from(c.company)] += 1;
            }
        }
        for (id, count) in (0..).zip(counts) {
            companies.set_count(id, count);
        }
        let companies_json = serde_json::to_string(companies.as_slice())
            .unwrap_or_else(|_| "[]".to_owned())
            .into_boxed_str();
        let by_slug = problems
            .iter()
            .enumerate()
            .map(|(i, p)| (p.slug.clone(), i))
            .collect();
        Self {
            topics: topics_by_count(&problems),
            search_index: SearchIndex::new(&problems),
            lists: Lists::build(&problems, companies.len()),
            companies_json,
            companies,
            problems,
            approaches,
            by_slug,
        }
    }

    /// The problem with this slug.
    #[must_use]
    pub fn problem(&self, slug: &str) -> Option<&Problem> {
        self.by_slug.get(slug).map(|&i| &self.problems[i])
    }

    /// The problem a list entry points at.
    #[must_use]
    pub fn problem_at(&self, entry: &ListEntry) -> &Problem {
        &self.problems[entry.problem as usize]
    }

    /// The worked approach for this slug, if one was written.
    #[must_use]
    pub fn approach(&self, slug: &str) -> Option<&Approach> {
        self.approaches.get(slug)
    }

    /// A problem in its JSON shape, company ids resolved.
    #[must_use]
    pub fn view<'a>(&'a self, problem: &'a Problem) -> ProblemView<'a> {
        problem.view(&self.companies)
    }

    /// `[{"slug", "name", "problems"}]` in picker order, serialized at load.
    #[must_use]
    pub fn companies_json(&self) -> &str {
        &self.companies_json
    }

    /// "any" or a known company slug.
    #[must_use]
    pub fn company_filter(&self, slug: &str) -> Option<CompanyFilter> {
        if slug == ANY_COMPANY {
            Some(CompanyFilter::Any)
        } else {
            self.companies.id(slug).map(CompanyFilter::Company)
        }
    }

    /// The company a request without a valid one gets: [`DEFAULT_COMPANY`], else any.
    #[must_use]
    pub fn default_company(&self) -> CompanyFilter {
        self.company_filter(DEFAULT_COMPANY)
            .unwrap_or(CompanyFilter::Any)
    }

    /// The company of a request, leniently: missing or unknown means the default.
    #[must_use]
    pub fn company_or_default(&self, slug: Option<&str>) -> CompanyFilter {
        slug.and_then(|s| self.company_filter(s))
            .unwrap_or_else(|| self.default_company())
    }

    /// The list of a request, leniently: an unknown company or period means the default
    /// ("google", "6m").
    #[must_use]
    pub fn list_id(&self, company: Option<&str>, period: Option<&str>) -> ListId {
        ListId {
            company: self.company_or_default(company),
            period: period.and_then(|p| p.parse().ok()).unwrap_or_default(),
        }
    }

    /// A list's entries, in new-card order.
    #[must_use]
    pub fn list(&self, id: ListId) -> &[ListEntry] {
        self.lists.get(id)
    }

    /// A list's problems, in new-card order.
    pub fn list_problems(&self, id: ListId) -> impl Iterator<Item = &Problem> + Clone {
        self.list(id).iter().map(|e| self.problem_at(e))
    }

    /// Ranked search hits for a free-text query; see [`SearchIndex::search`].
    #[must_use]
    pub fn search(&self, query: &str, limit: usize) -> Vec<SearchHit<'_>> {
        self.search_index.search(query, limit)
    }
}

/// Builders over the real data files, for tests across modules.
#[cfg(test)]
pub(crate) mod testdata {
    use std::path::{Path, PathBuf};
    use std::sync::LazyLock;

    use super::Content;

    /// The problems file under test.
    pub const PROBLEMS: &str = "problems.json";

    /// The real problems and approaches.
    pub static CONTENT: LazyLock<Content> = LazyLock::new(|| {
        Content::load(&data(PROBLEMS), &data("approaches.json")).expect("load the problems file")
    });

    /// Path of a file in `data/`.
    pub fn data(name: &str) -> PathBuf {
        Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../data")
            .join(name)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::Period;
    use crate::model::fixtures::{GOOGLE, companies, problem};

    #[test]
    fn sorts_topics_by_count_and_indexes_slugs() {
        let mut a = problem(1);
        a.topics = vec!["Graph".into(), "Array".into()];
        let mut b = problem(2);
        b.topics = vec!["Tree".into(), "Array".into()];
        let content = Content::new(companies(), vec![a, b], HashMap::new());
        assert_eq!(content.topics, ["Array", "Graph", "Tree"]);
        assert_eq!(content.problem("p2").map(|p| p.id), Some(2));
        assert!(content.problem("nope").is_none());
        assert_eq!(
            content.companies_json(),
            r#"[{"slug":"google","name":"Google","problems":2},{"slug":"meta","name":"Meta","problems":0}]"#
        );
    }

    #[test]
    fn parses_list_selections_leniently() {
        let content = Content::new(companies(), vec![problem(1)], HashMap::new());
        let google = CompanyFilter::Company(GOOGLE);
        let id = content.list_id(Some("meta"), Some("all"));
        assert_eq!(
            (id.company, id.period),
            (CompanyFilter::Company(1), Period::All)
        );
        let id = content.list_id(Some("acme"), Some("1y"));
        assert_eq!((id.company, id.period), (google, Period::Months6));
        assert_eq!(
            content.list_id(Some("any"), None).company,
            CompanyFilter::Any
        );
        assert_eq!(content.default_company(), google);
        assert_eq!(Content::default().default_company(), CompanyFilter::Any);
    }

    #[test]
    fn missing_files_load_empty() {
        let none = Path::new("/nonexistent/data/x.json");
        let content = Content::load(none, none).expect("load");
        assert!(content.problems.is_empty() && content.topics.is_empty());
        assert_eq!(content.companies_json(), "[]");
    }

    #[test]
    fn loads_the_company_file() {
        let content = &*testdata::CONTENT;
        assert!(content.problems.len() >= 3000);
        assert_eq!(content.companies.get(0).slug, "google");
        let two = content.problem("two-sum").expect("two-sum");
        let json = serde_json::to_value(content.view(two)).expect("serialize");
        assert_eq!(json["companies"]["google"]["6m"]["rank"], 1);
        assert!(json.get("asked").is_none());
        let classic = content
            .problems
            .iter()
            .find(|p| p.companies.is_empty())
            .expect("a classic-only problem");
        let json = serde_json::to_value(content.view(classic)).expect("serialize");
        assert_eq!(json["companies"], serde_json::json!({}));
        assert!(content.approach("two-sum").is_some());
        let declared: serde_json::Value =
            serde_json::from_str(content.companies_json()).expect("companies json");
        assert_eq!(
            declared[0]["problems"],
            content
                .list(ListId {
                    company: CompanyFilter::Company(GOOGLE),
                    period: Period::All,
                })
                .len()
        );
    }

    #[test]
    fn company_json_round_trips_the_file() {
        let path = testdata::data(testdata::PROBLEMS);
        let file: serde_json::Value =
            serde_json::from_slice(&std::fs::read(path).expect("read")).expect("parse");
        let content = &*testdata::CONTENT;
        for (raw, problem) in file["problems"]
            .as_array()
            .expect("problems")
            .iter()
            .zip(&content.problems)
        {
            // Through text: a `Value` would widen the f32 frequencies.
            let text = serde_json::to_string(&content.view(problem)).expect("serialize");
            let view: serde_json::Value = serde_json::from_str(&text).expect("parse");
            assert_eq!(view["companies"], raw["companies"], "{}", problem.slug);
            assert_eq!(view["slug"], raw["slug"]);
        }
    }
}
