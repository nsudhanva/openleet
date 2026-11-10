//! Free-text problem search: number, title (words, prefixes, acronym, small typos),
//! difficulty, topic and statement text (port of `web/src/lib/search.ts`).

use serde::Serialize;
use unicode_normalization::UnicodeNormalization;

use crate::model::{Difficulty, Problem};

/// Where a hit matched, strongest first. A hit reports its weakest required match.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum SearchField {
    /// The LeetCode number.
    Number,
    /// The title.
    Title,
    /// The difficulty name.
    Difficulty,
    /// A topic tag.
    Topic,
    /// The problem statement.
    Statement,
}

/// One search result.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct SearchHit<'a> {
    /// Problem slug.
    pub slug: &'a str,
    /// LeetCode number.
    pub id: u32,
    /// 6-month Google rank, or `100000 + id` for classic-only problems.
    pub rank: u32,
    /// Display title.
    pub title: &'a str,
    /// Difficulty.
    pub difficulty: Difficulty,
    /// The weakest field a query word matched.
    pub field: SearchField,
    /// Statement excerpt around the match, for statement-only hits.
    pub snippet: Option<String>,
}

/// One problem, preprocessed for matching.
#[derive(Debug)]
struct Doc {
    slug: String,
    id: u32,
    rank: u32,
    display_title: String,
    difficulty: Difficulty,
    /// Normalized title.
    title: String,
    title_words: Vec<String>,
    /// First letter of every title word.
    acronym: String,
    topic_words: Vec<String>,
    /// Lowercase difficulty name.
    difficulty_word: &'static str,
    /// Statement as plain text, for snippets.
    plain: String,
    /// Normalized statement padded with spaces, for word-prefix matching.
    text: String,
}

/// Search index over the problem list, built once at load.
#[derive(Debug, Default)]
pub struct SearchIndex {
    docs: Vec<Doc>,
}

const SNIPPET_RADIUS: usize = 60;
/// Score of a LeetCode-number match; beats everything else.
const NUMBER_SCORE: u32 = 10_000;
/// Score of an acronym match ("lis" for Longest Increasing Subsequence).
const ACRONYM_SCORE: u32 = 300;
/// Bonus when the whole query is the title.
const EXACT_TITLE_BONUS: u32 = 500;
/// Bonus when the title starts with the whole query.
const TITLE_PREFIX_BONUS: u32 = 200;

/// Whitespace as JavaScript's `\s` and `String.prototype.trim` define it.
const fn is_js_space(c: char) -> bool {
    matches!(
        c,
        '\t' | '\n' | '\u{0B}' | '\u{0C}' | '\r' | ' ' | '\u{A0}' | '\u{1680}' | '\u{2000}'
            ..='\u{200A}'
                | '\u{2028}'
                | '\u{2029}'
                | '\u{202F}'
                | '\u{205F}'
                | '\u{3000}'
                | '\u{FEFF}'
    )
}

/// Lowercase ASCII letters and digits, every other run turned into one space, accents
/// dropped: "Café-Latte" becomes "cafe latte".
#[must_use]
pub fn normalize(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    let mut gap = false;
    for c in text.chars().flat_map(char::to_lowercase).nfkd() {
        if ('\u{300}'..='\u{36F}').contains(&c) {
            continue;
        }
        if c.is_ascii_lowercase() || c.is_ascii_digit() {
            if gap && !out.is_empty() {
                out.push(' ');
            }
            gap = false;
            out.push(c);
        } else {
            gap = true;
        }
    }
    out
}

fn entity(name: &str) -> char {
    match name {
        "&lt;" => '<',
        "&gt;" => '>',
        "&amp;" => '&',
        "&quot;" => '"',
        "&#39;" => '\'',
        _ => ' ',
    }
}

/// HTML to plain text: tags become spaces, known entities their characters (others a
/// space), whitespace runs one space, trimmed.
fn plain_text(html: &str) -> String {
    let mut out = String::with_capacity(html.len());
    let mut gap = false;
    let mut emit = |c: char, out: &mut String| {
        if is_js_space(c) {
            gap = true;
        } else {
            if gap && !out.is_empty() {
                out.push(' ');
            }
            gap = false;
            out.push(c);
        }
    };
    let mut rest = html;
    while let Some(c) = rest.chars().next() {
        let skip = match c {
            // `<[^>]+>`
            '<' => rest[1..]
                .find('>')
                .filter(|&end| end > 0)
                .map(|end| end + 2),
            // `&[a-z#0-9]+;`
            '&' => {
                let body = rest[1..]
                    .bytes()
                    .take_while(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || *b == b'#')
                    .count();
                (body > 0 && rest.as_bytes().get(body + 1) == Some(&b';')).then_some(body + 2)
            }
            _ => None,
        };
        if let Some(len) = skip {
            emit(if c == '<' { ' ' } else { entity(&rest[..len]) }, &mut out);
            rest = &rest[len..];
        } else {
            emit(c, &mut out);
            rest = &rest[c.len_utf8()..];
        }
    }
    out
}

/// Reusable rows for [`within_edits`], so matching allocates nothing per word.
#[derive(Default)]
struct EditRows {
    older: Vec<usize>,
    previous: Vec<usize>,
    current: Vec<usize>,
}

/// Edit distance where a swap of neighbors counts once ("rian" to "rain"), capped at `max`.
fn within_edits(a: &[u8], b: &[u8], max: usize, rows: &mut EditRows) -> bool {
    if a.len().abs_diff(b.len()) > max {
        return false;
    }
    let EditRows {
        older,
        previous,
        current,
    } = rows;
    older.clear();
    previous.clear();
    previous.extend(0..=b.len());
    for i in 1..=a.len() {
        current.clear();
        current.push(i);
        for j in 1..=b.len() {
            let cost = usize::from(a[i - 1] != b[j - 1]);
            let mut best = (previous[j] + 1)
                .min(current[j - 1] + 1)
                .min(previous[j - 1] + cost);
            if i > 1 && j > 1 && a[i - 1] == b[j - 2] && a[i - 2] == b[j - 1] {
                best = best.min(older[j - 2] + 1);
            }
            current.push(best);
        }
        if current.iter().min().is_some_and(|&m| m > max) {
            return false;
        }
        std::mem::swap(older, previous);
        std::mem::swap(previous, current);
    }
    previous[b.len()] <= max
}

/// Best match of one query token in a document, or `None` when it matches nowhere.
fn match_token(doc: &Doc, token: &str, rows: &mut EditRows) -> Option<(u32, SearchField)> {
    if doc.title_words.iter().any(|w| w == token) {
        return Some((60, SearchField::Title));
    }
    if doc.title_words.iter().any(|w| w.starts_with(token)) {
        return Some((45, SearchField::Title));
    }
    if doc.title.contains(token) {
        return Some((30, SearchField::Title));
    }
    let typos = if token.len() >= 8 { 2 } else { 1 };
    if token.len() >= 4
        && doc
            .title_words
            .iter()
            .any(|w| within_edits(token.as_bytes(), w.as_bytes(), typos, rows))
    {
        return Some((25, SearchField::Title));
    }
    if doc.difficulty_word == token {
        return Some((20, SearchField::Difficulty));
    }
    if doc.topic_words.iter().any(|w| w.starts_with(token)) {
        return Some((15, SearchField::Topic));
    }
    // `text` is padded, so " token" finds a word starting with it.
    let found = doc
        .text
        .match_indices(token)
        .any(|(at, _)| at > 0 && doc.text.as_bytes()[at - 1] == b' ');
    found.then_some((5, SearchField::Statement))
}

/// Byte offset of the start of the `n`th character after `at`, or the end of `text`.
fn chars_forward(text: &str, at: usize, n: usize) -> usize {
    text[at..]
        .char_indices()
        .nth(n)
        .map_or(text.len(), |(i, _)| at + i)
}

/// Byte offset `n` characters before `at`, or 0.
fn chars_back(text: &str, at: usize, n: usize) -> usize {
    match n.checked_sub(1) {
        None => at,
        Some(k) => text[..at].char_indices().rev().nth(k).map_or(0, |(i, _)| i),
    }
}

/// Statement excerpt of about `SNIPPET_RADIUS` characters either side of the token's first
/// case-insensitive occurrence, or its opening when the token is not there verbatim.
fn snippet(plain: &str, token: &str) -> String {
    let at = plain
        .as_bytes()
        .windows(token.len())
        .position(|w| w.eq_ignore_ascii_case(token.as_bytes()));
    let Some(at) = at else {
        return plain[..chars_forward(plain, 0, 2 * SNIPPET_RADIUS)].to_owned();
    };
    let start = chars_back(plain, at, SNIPPET_RADIUS);
    let end = chars_forward(plain, at + token.len(), SNIPPET_RADIUS);
    let mut out = String::with_capacity(end - start + 6);
    if start > 0 {
        out.push('…');
    }
    out.push_str(&plain[start..end]);
    if end < plain.len() {
        out.push('…');
    }
    out
}

/// The problem number in queries such as "1", "#1", "lc 1", "LeetCode 1", "no. 1" or
/// "problem 1". `raw` must already be trimmed.
fn number_query(raw: &str) -> Option<u32> {
    const PREFIXES: [&str; 7] = ["lc", "leetcode", "#", "no.", "no", "problem", ""];
    let lower = raw.to_ascii_lowercase();
    PREFIXES.iter().find_map(|prefix| {
        let digits = lower.strip_prefix(prefix)?.trim_start_matches(is_js_space);
        let valid = (1..=5).contains(&digits.len()) && digits.bytes().all(|b| b.is_ascii_digit());
        valid.then(|| digits.parse().ok()).flatten()
    })
}

/// One scored document before hits are built.
struct Scored<'d, 'q> {
    doc: &'d Doc,
    score: u32,
    field: SearchField,
    /// The query word behind `field`, for the statement snippet.
    token: Option<&'q str>,
}

impl SearchIndex {
    /// Preprocesses every problem.
    #[must_use]
    pub fn new(problems: &[Problem]) -> Self {
        let docs = problems
            .iter()
            .map(|problem| {
                let title = normalize(&problem.title);
                let title_words: Vec<String> = title.split(' ').map(str::to_owned).collect();
                let acronym = title_words
                    .iter()
                    .filter_map(|w| w.chars().next())
                    .collect();
                let topic_words = normalize(&problem.topics.join(" "))
                    .split(' ')
                    .map(str::to_owned)
                    .collect();
                let plain = plain_text(problem.description.as_deref().unwrap_or(""));
                let text = format!(" {} ", normalize(&plain));
                Doc {
                    slug: problem.slug.clone(),
                    id: problem.id,
                    rank: problem.rank(),
                    display_title: problem.title.clone(),
                    difficulty: problem.difficulty,
                    title,
                    title_words,
                    acronym,
                    topic_words,
                    difficulty_word: match problem.difficulty {
                        Difficulty::Easy => "easy",
                        Difficulty::Medium => "medium",
                        Difficulty::Hard => "hard",
                    },
                    plain,
                    text,
                }
            })
            .collect();
        Self { docs }
    }

    /// Ranks problems for a free-text query. Every word must match somewhere; ties go to
    /// the problem Google asks more often. At most `limit` hits.
    #[must_use]
    pub fn search(&self, query: &str, limit: usize) -> Vec<SearchHit<'_>> {
        let raw = query.trim_matches(is_js_space);
        let q = normalize(raw);
        if q.is_empty() {
            return Vec::new();
        }
        let tokens: Vec<&str> = q.split(' ').collect();
        let compact: String = tokens.concat();
        let number = number_query(raw);
        let mut rows = EditRows::default();
        let mut matches: Vec<(u32, SearchField)> = Vec::with_capacity(tokens.len());

        let mut scored: Vec<Scored<'_, '_>> = Vec::new();
        for doc in &self.docs {
            if number == Some(doc.id) {
                scored.push(Scored {
                    doc,
                    score: NUMBER_SCORE,
                    field: SearchField::Number,
                    token: None,
                });
                continue;
            }
            if compact.len() >= 2 && doc.acronym == compact {
                scored.push(Scored {
                    doc,
                    score: ACRONYM_SCORE,
                    field: SearchField::Title,
                    token: None,
                });
                continue;
            }
            matches.clear();
            let all = tokens.iter().all(|t| {
                match_token(doc, t, &mut rows)
                    .map(|m| matches.push(m))
                    .is_some()
            });
            if !all {
                continue;
            }
            let mut score: u32 = matches.iter().map(|&(s, _)| s).sum();
            // The last token with the weakest field explains the hit.
            let (field, token) = matches.iter().zip(&tokens).fold(
                (SearchField::Number, tokens[0]),
                |acc, (&(_, f), &t)| {
                    if f >= acc.0 { (f, t) } else { acc }
                },
            );
            if doc.title == q {
                score += EXACT_TITLE_BONUS;
            } else if doc.title.starts_with(q.as_str()) {
                score += TITLE_PREFIX_BONUS;
            }
            scored.push(Scored {
                doc,
                score,
                field,
                token: Some(token),
            });
        }

        scored.sort_by(|a, b| b.score.cmp(&a.score).then(a.doc.rank.cmp(&b.doc.rank)));
        scored.truncate(limit);
        scored
            .into_iter()
            .map(
                |Scored {
                     doc, field, token, ..
                 }| SearchHit {
                    slug: &doc.slug,
                    id: doc.id,
                    rank: doc.rank,
                    title: &doc.display_title,
                    difficulty: doc.difficulty,
                    field,
                    snippet: token
                        .filter(|_| field == SearchField::Statement)
                        .map(|t| snippet(&doc.plain, t)),
                },
            )
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use std::path::Path;
    use std::sync::LazyLock;

    use super::*;
    use crate::content::Content;

    static CONTENT: LazyLock<Content> = LazyLock::new(|| {
        let dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("../data");
        Content::load(&dir).expect("load data/")
    });

    fn top(query: &str) -> Option<&'static str> {
        CONTENT
            .search_index
            .search(query, 5)
            .first()
            .map(|h| h.slug)
    }

    #[test]
    fn normalizes_text() {
        assert_eq!(normalize("  Café-Latte  2 "), "cafe latte 2");
        assert_eq!(normalize("!!!"), "");
    }

    #[test]
    fn strips_html() {
        assert_eq!(
            plain_text("<p>a&nbsp;&lt;b&gt; &amp;&#39;x&bogus; <>\u{a0}c</p>"),
            "a <b> &'x <> c"
        );
    }

    #[test]
    fn counts_swaps_once() {
        let mut rows = EditRows::default();
        assert!(within_edits(b"rian", b"rain", 1, &mut rows));
        assert!(!within_edits(b"rian", b"ruin", 0, &mut rows));
        assert!(within_edits(b"kitten", b"sitten", 1, &mut rows));
        assert!(!within_edits(b"kitten", b"sitting", 2, &mut rows));
        assert!(!within_edits(b"abcd", b"wxyz", 2, &mut rows));
    }

    #[test]
    fn parses_number_queries() {
        for q in [
            "1",
            "#1",
            "lc 1",
            "LC1",
            "LeetCode 1",
            "no. 1",
            "problem 1",
            "0001",
        ] {
            assert_eq!(number_query(q), Some(1), "{q}");
        }
        assert_eq!(number_query("123456"), None);
        assert_eq!(number_query("two 1"), None);
    }

    #[test]
    fn finds_two_sum_by_number_or_title() {
        for q in ["1", "#1", "lc 1", "LC1", "two sum", "Two Sum"] {
            assert_eq!(top(q), Some("two-sum"), "{q}");
        }
    }

    #[test]
    fn matches_title_prefixes_acronyms_and_typos() {
        assert_eq!(top("lru"), Some("lru-cache"));
        assert_eq!(top("lis"), Some("longest-increasing-subsequence"));
        assert_eq!(top("trapping rian water"), Some("trapping-rain-water"));
        assert_eq!(top("median sorted"), Some("median-of-two-sorted-arrays"));
    }

    #[test]
    fn needs_every_word_and_searches_topics_difficulty_and_statements() {
        let hits = CONTENT.search_index.search("hard dynamic", 50);
        assert!(hits.len() > 5);
        for hit in &hits {
            let problem = CONTENT.problem(hit.slug).expect("known slug");
            assert_eq!(problem.difficulty, Difficulty::Hard);
            assert!(problem.has_topic("Dynamic Programming"));
        }
        let hits = CONTENT.search_index.search("reverse order linked", 50);
        let statement = hits
            .iter()
            .find(|h| h.slug == "add-two-numbers")
            .expect("hit");
        assert_eq!(statement.field, SearchField::Statement);
        let snippet = statement
            .snippet
            .as_deref()
            .unwrap_or_default()
            .to_lowercase();
        assert!(snippet.contains("reverse order"), "{snippet}");
    }

    #[test]
    fn classic_problems_rank_after_google_ones() {
        let hits = CONTENT.search_index.search("1000", 5);
        let hit = hits.first().expect("problem 1000");
        assert_eq!((hit.id, hit.rank), (1000, 101_000));
        assert_eq!(hit.field, SearchField::Number);
    }

    #[test]
    fn empty_queries_find_nothing() {
        assert_eq!(CONTENT.search_index.search("  ?! ", 5).len(), 0);
    }
}
