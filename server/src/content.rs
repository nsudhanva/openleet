//! The read-only study content, loaded once and kept in memory
//! (port of `web/src/server/content.ts`).

use std::cmp::Reverse;
use std::collections::HashMap;
use std::io::ErrorKind;
use std::path::Path;

use anyhow::Context as _;
use serde::Deserialize;
use serde::de::DeserializeOwned;

use crate::model::{Approach, Problem};
use crate::search::{SearchHit, SearchIndex};

/// Problems, approaches and the indexes built from them.
#[derive(Debug, Default)]
pub struct Content {
    /// Every problem: Google ones in 6-month rank order, then classic-only ones.
    pub problems: Vec<Problem>,
    /// Worked approach per slug.
    pub approaches: HashMap<String, Approach>,
    /// Every topic in the list, most common first (ties in order of first use).
    pub topics: Vec<String>,
    /// Search index over `problems`.
    pub search_index: SearchIndex,
    /// Position in `problems` per slug.
    by_slug: HashMap<String, usize>,
}

/// The shape of `problems.json`; its `sources` are not needed at run time.
#[derive(Deserialize)]
struct ProblemsFile {
    problems: Vec<Problem>,
}

/// Parses `dir/name`, or returns `None` when the file does not exist.
fn read_json<T: DeserializeOwned>(dir: &Path, name: &str) -> anyhow::Result<Option<T>> {
    let path = dir.join(name);
    let bytes = match std::fs::read(&path) {
        Ok(bytes) => bytes,
        Err(error) if error.kind() == ErrorKind::NotFound => return Ok(None),
        Err(error) => return Err(error).with_context(|| format!("reading {}", path.display())),
    };
    serde_json::from_slice(&bytes)
        .map(Some)
        .with_context(|| format!("parsing {}", path.display()))
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
    counts.sort_by_key(|&(_, n)| Reverse(n));
    counts
        .into_iter()
        .map(|(topic, _)| topic.to_owned())
        .collect()
}

impl Content {
    /// Loads `problems.json` and `approaches.json` from `data_dir` (built by the Python tools
    /// at the repo root). A missing file counts as empty; an unreadable one is an error.
    ///
    /// # Errors
    /// When a file exists but cannot be read or parsed.
    pub fn load(data_dir: &Path) -> anyhow::Result<Self> {
        let problems = read_json::<ProblemsFile>(data_dir, "problems.json")?
            .map(|file| file.problems)
            .unwrap_or_default();
        let approaches = read_json(data_dir, "approaches.json")?.unwrap_or_default();
        Ok(Self::new(problems, approaches))
    }

    /// Builds the indexes over already parsed content.
    #[must_use]
    pub fn new(problems: Vec<Problem>, approaches: HashMap<String, Approach>) -> Self {
        let by_slug = problems
            .iter()
            .enumerate()
            .map(|(i, p)| (p.slug.clone(), i))
            .collect();
        Self {
            topics: topics_by_count(&problems),
            search_index: SearchIndex::new(&problems),
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

    /// The worked approach for this slug, if one was written.
    #[must_use]
    pub fn approach(&self, slug: &str) -> Option<&Approach> {
        self.approaches.get(slug)
    }

    /// Ranked search hits for a free-text query; see [`SearchIndex::search`].
    #[must_use]
    pub fn search(&self, query: &str, limit: usize) -> Vec<SearchHit<'_>> {
        self.search_index.search(query, limit)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::fixtures::problem;

    #[test]
    fn sorts_topics_by_count_and_indexes_slugs() {
        let mut a = problem(1);
        a.topics = vec!["Graph".into(), "Array".into()];
        let mut b = problem(2);
        b.topics = vec!["Tree".into(), "Array".into()];
        let content = Content::new(vec![a, b], HashMap::new());
        assert_eq!(content.topics, ["Array", "Graph", "Tree"]);
        assert_eq!(content.problem("p2").map(|p| p.id), Some(2));
        assert!(content.problem("nope").is_none());
    }

    #[test]
    fn missing_files_load_empty() {
        let content = Content::load(Path::new("/nonexistent/data")).expect("load");
        assert!(content.problems.is_empty() && content.topics.is_empty());
    }

    #[test]
    fn loads_the_real_data() {
        let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("../data");
        let content = Content::load(&dir).expect("load");
        assert!(content.problems.len() >= 1175);
        let classic = content
            .problems
            .iter()
            .find(|p| !p.is_google())
            .expect("a classic-only problem");
        let json = serde_json::to_value(classic).expect("serialize");
        assert_eq!(json["asked"], serde_json::json!({}));
        assert!(content.approach("two-sum").is_some());
    }
}
