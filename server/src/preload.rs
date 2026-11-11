//! What a page of the web app loads first, so the server can preload it with the page: the
//! API requests of its route loaders (web/src/routes, their queries from
//! web/src/lib/schemas.ts) and its route's code. The browser then fetches both alongside the
//! app's main code instead of after it.
//!
//! A preload helps only when the app later asks for the same URL, byte for byte; otherwise
//! the browser fetches twice and warns. So this mirrors how the app's router reads search
//! params, and leaves a request out whenever it cannot be sure. web/src/lib/page-loads.json
//! holds the cases both sides are tested against.

use std::collections::HashMap;
use std::fmt::Write as _;
use std::str::FromStr;

use openleet::model::{Difficulty, Period};
use openleet::plan::{PlanOrder, PlanStatus};
use openleet::scheduler::StudySet;
use openleet::search::is_js_space;

/// The router's default company (web/src/lib/companies.ts).
const DEFAULT_COMPANY: &str = "google";
/// Longest topic and search query the app keeps (web/src/lib/schemas.ts).
const MAX_TOPIC: usize = 100;
const MAX_QUERY: usize = 200;
/// Problem slugs are short; a longer path segment is no problem's.
const MAX_SLUG: usize = 128;

/// `<link rel="preload">` tags for the data the page at `path?query` loads first. (Its route's
/// code is preloaded too, by the version of index.html made for that route: build.rs.)
pub fn links(path: &str, query: Option<&str>) -> String {
    let mut links = String::new();
    for url in urls(path, query) {
        // URLs are percent-encoded: `&` is the only character to escape in an attribute.
        let href = url.replace('&', "&amp;");
        let _ = write!(
            links,
            r#"<link rel="preload" as="fetch" crossorigin href="{href}">"#
        );
    }
    links
}

/// The route file (web/src/routes) that renders `path`.
pub fn route(path: &str) -> Option<&'static str> {
    match path {
        "/" => Some("index"),
        "/problems" => Some("problems"),
        "/progress" => Some("progress"),
        "/about" => Some("about"),
        _ => path
            .strip_prefix("/code/")
            .filter(|slug| !slug.is_empty() && !slug.contains('/'))
            .map(|_| "code.$slug"),
    }
}

/// The API requests the page's route loaders make first, in order: the root route's (every
/// page), then the page's own.
pub fn urls(path: &str, query: Option<&str>) -> Vec<String> {
    let params = Params::parse(query.unwrap_or_default());
    let company = params.company();
    let mut urls = vec![
        api("/api/readiness", &[("company", Some(company.clone()))]),
        "/api/companies".to_owned(),
    ];
    match path {
        "/" => urls.extend(params.deck(company)),
        "/problems" => {
            urls.extend(params.problems(company));
            urls.push("/api/plans".to_owned());
        }
        "/progress" => urls.push(api("/api/report", &[("company", Some(company))])),
        _ => {
            if let Some(slug) = path.strip_prefix("/code/").filter(|s| is_slug(s, MAX_SLUG)) {
                urls.extend([
                    format!("/api/problems/{slug}"),
                    format!("/api/code/{slug}"),
                    api("/api/submissions", &[("slug", Some(slug.to_owned()))]),
                ]);
            }
        }
    }
    urls
}

/// A path with a query, as the app's API client writes it: unset params left out, the rest
/// encoded like `URLSearchParams`.
fn api(path: &str, query: &[(&str, Option<String>)]) -> String {
    let mut serializer = form_urlencoded::Serializer::new(String::new());
    for (key, value) in query {
        if let Some(value) = value {
            serializer.append_pair(key, value);
        }
    }
    let query = serializer.finish();
    if query.is_empty() {
        path.to_owned()
    } else {
        format!("{path}?{query}")
    }
}

fn is_slug(text: &str, max: usize) -> bool {
    !text.is_empty()
        && text.len() <= max
        && text
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
}

/// A search param's value as the router parses it: canonical numbers, `true` and `false`, and
/// text that parses as JSON become values of their own type.
#[derive(Debug, Clone, PartialEq)]
enum Value {
    Text(String),
    /// A number, with its JavaScript `String()` when this can tell.
    Number(Option<String>),
    /// An array (a repeated param), boolean, null or object.
    Other,
    /// JSON that JavaScript and `serde_json` might read differently.
    Unsure,
}

impl Value {
    /// The router's `decode` (qss) and then its `JSON.parse` of string values.
    fn parse(raw: String) -> Self {
        if raw.is_empty() {
            return Self::Text(raw);
        }
        if raw == "true" || raw == "false" {
            return Self::Other;
        }
        // The router tries JSON.parse only on text that can start JSON. A canonical number
        // ("42") becomes a number before that; JSON.parse gives the same.
        let first = raw.chars().next().unwrap_or_default();
        let json_start = is_js_space(first)
            || "\"[{-".contains(first)
            || first.is_ascii_digit()
            || ["fa", "nu", "tr"].iter().any(|p| raw.starts_with(p));
        if !json_start {
            return Self::Text(raw);
        }
        match serde_json::from_str::<serde_json::Value>(&raw) {
            Ok(serde_json::Value::String(text)) => Self::Text(text),
            Ok(serde_json::Value::Number(number)) => Self::Number(js_string(&number)),
            Ok(_) => Self::Other,
            // JSON.parse failed too and the text stays text, unless it is JSON serde_json
            // refuses and JavaScript takes: huge numbers, lone surrogates, deep nesting.
            Err(_) => {
                let trimmed = raw.trim_start_matches([' ', '\t', '\n', '\r']);
                if trimmed.starts_with(['"', '[', '{']) || looks_numeric(trimmed) {
                    Self::Unsure
                } else {
                    Self::Text(raw)
                }
            }
        }
    }

    /// The text of a free-text filter (`text()` in schemas.ts): trimmed, cut to `max` UTF-16
    /// units and trimmed again; `Ok(None)` when there is none, `Err` when this cannot tell.
    fn text(&self, max: usize) -> Result<Option<String>, ()> {
        let raw = match self {
            Self::Text(text) => text.as_str(),
            Self::Number(Some(text)) => text.as_str(),
            Self::Other => return Ok(None),
            Self::Number(None) | Self::Unsure => return Err(()),
        };
        let mut cut = String::new();
        let mut units = 0;
        for c in js_trim(raw).chars() {
            units += c.len_utf16();
            if units > max {
                // JavaScript would keep half of a surrogate pair.
                if units - c.len_utf16() < max {
                    return Err(());
                }
                break;
            }
            cut.push(c);
        }
        let text = js_trim(&cut);
        Ok((!text.is_empty()).then(|| text.to_owned()))
    }

    /// The variant the value spells (`oneOf()` in schemas.ts).
    fn one_of<T: FromStr>(&self) -> Option<T> {
        match self {
            Self::Text(text) => text.parse().ok(),
            _ => None,
        }
    }
}

/// JavaScript's `String(number)` for the whole numbers it prints plainly; `None` otherwise.
fn js_string(number: &serde_json::Number) -> Option<String> {
    const MAX_SAFE: f64 = 9_007_199_254_740_991.0;
    let value = number.as_f64()?;
    // Exact for whole numbers up to 2^53; -0 prints as "0", in JavaScript too.
    let whole = value as i64;
    (value.fract() == 0.0 && value.abs() <= MAX_SAFE).then(|| whole.to_string())
}

fn looks_numeric(text: &str) -> bool {
    text.trim_end()
        .trim_start_matches('-')
        .starts_with(|c: char| c.is_ascii_digit())
        && text
            .trim_end()
            .bytes()
            .all(|b| b.is_ascii_digit() || b"+-.eE".contains(&b))
}

fn js_trim(text: &str) -> &str {
    text.trim_matches(is_js_space)
}

/// A page's search params, parsed like the router does.
struct Params(HashMap<String, Value>);

impl Params {
    fn parse(query: &str) -> Self {
        let mut params = HashMap::new();
        for (key, value) in form_urlencoded::parse(query.as_bytes()) {
            params
                .entry(key.into_owned())
                // A repeated param becomes an array.
                .and_modify(|v| *v = Value::Other)
                .or_insert_with(|| Value::parse(value.into_owned()));
        }
        Self(params)
    }

    fn get(&self, key: &str) -> Option<&Value> {
        self.0.get(key)
    }

    fn one_of<T: FromStr>(&self, key: &str) -> Option<T> {
        self.get(key).and_then(Value::one_of)
    }

    fn text(&self, key: &str, max: usize) -> Result<Option<String>, ()> {
        self.get(key).map_or(Ok(None), |v| v.text(max))
    }

    /// `parseCompanySearch`: a slug, else the default company.
    fn company(&self) -> String {
        match self.get("company") {
            Some(Value::Text(slug)) if is_slug(slug, usize::MAX) => slug.clone(),
            _ => DEFAULT_COMPANY.to_owned(),
        }
    }

    /// The study page's `deckQuery`.
    fn deck(&self, company: String) -> Option<String> {
        let set: StudySet = self.one_of("set").unwrap_or_default();
        Some(api(
            "/api/deck",
            &[
                ("company", Some(company)),
                ("set", Some(set.to_string())),
                ("period", Some(self.period())),
                ("topic", self.text("topic", MAX_TOPIC).ok()?),
                ("difficulty", self.difficulty()),
                ("slug", self.text("slug", usize::MAX).ok()?),
            ],
        ))
    }

    /// The problem table's `problemsQuery`.
    fn problems(&self, company: String) -> Option<String> {
        // The table leaves out the plan's "all" status and "rank" order: every problem, in
        // list order (lib/plan.ts).
        let status = self
            .one_of::<PlanStatus>("status")
            .filter(|&s| s != PlanStatus::All);
        let order = self
            .one_of::<PlanOrder>("order")
            .filter(|&o| o != PlanOrder::Rank);
        Some(api(
            "/api/problems",
            &[
                ("company", Some(company)),
                ("period", Some(self.period())),
                ("topic", self.text("topic", MAX_TOPIC).ok()?),
                ("difficulty", self.difficulty()),
                ("status", status.map(|s| s.to_string())),
                ("order", order.map(|o| o.to_string())),
                ("q", self.text("q", MAX_QUERY).ok()?),
            ],
        ))
    }

    fn period(&self) -> String {
        self.one_of::<Period>("period")
            .unwrap_or_default()
            .to_string()
    }

    fn difficulty(&self) -> Option<String> {
        self.one_of::<Difficulty>("difficulty")
            .map(|d| d.to_string())
    }
}

#[cfg(test)]
mod tests {
    use serde::Deserialize;

    use super::*;

    #[derive(Deserialize)]
    struct Case {
        page: String,
        fetches: Vec<String>,
    }

    fn split(page: &str) -> (&str, Option<&str>) {
        page.split_once('?')
            .map_or((page, None), |(path, query)| (path, Some(query)))
    }

    /// The same cases as the web app's test (web/src/lib/page-loads.test.ts), which checks
    /// that the app requests exactly these URLs.
    #[test]
    fn preloads_what_the_app_loads() {
        let cases: Vec<Case> =
            serde_json::from_str(include_str!("../../web/src/lib/page-loads.json")).expect("cases");
        for case in cases {
            let (path, query) = split(&case.page);
            assert_eq!(urls(path, query), case.fetches, "{}", case.page);
        }
    }

    #[test]
    fn leaves_out_what_it_cannot_be_sure_of() {
        fn page(page: &str) -> Vec<String> {
            let (path, query) = split(page);
            urls(path, query)
        }
        // Numbers JavaScript prints its own way, and JSON serde_json refuses.
        // The problem table's plans need no query, so they are preloaded all the same.
        for value in ["1.5", "1e21", "1e400", "%5B%5B", "%22%5Cud800%22"] {
            assert_eq!(page(&format!("/?topic={value}")).len(), 2, "{value}");
            assert_eq!(
                page(&format!("/problems?q={value}"))[2..],
                ["/api/plans"],
                "{value}"
            );
        }
        // Half of a surrogate pair at the cut.
        let q = format!("{}%F0%9F%98%80", "a".repeat(MAX_QUERY - 1));
        assert_eq!(page(&format!("/problems?q={q}"))[2..], ["/api/plans"]);
        // Such values are no company, set or period either way.
        assert_eq!(
            page("/progress?company=1.5"),
            [
                "/api/readiness?company=google",
                "/api/companies",
                "/api/report?company=google"
            ]
        );
        // Not a problem's slug.
        assert_eq!(page("/code/Two%20Sum").len(), 2);
        assert_eq!(page("/code/two-sum/x").len(), 2);
    }

    #[test]
    fn knows_the_routes() {
        assert_eq!(route("/"), Some("index"));
        assert_eq!(route("/code/two-sum"), Some("code.$slug"));
        assert_eq!(route("/code/"), None);
        assert_eq!(route("/code/a/b"), None);
        assert_eq!(route("/nope"), None);
    }

    #[test]
    fn writes_link_tags() {
        let data = |page| {
            let links = links(page, None);
            links[..links
                .find("<link rel=\"modulepreload\"")
                .unwrap_or(links.len())]
                .to_owned()
        };
        assert_eq!(
            data("/progress"),
            concat!(
                r#"<link rel="preload" as="fetch" crossorigin href="/api/readiness?company=google">"#,
                r#"<link rel="preload" as="fetch" crossorigin href="/api/companies">"#,
                r#"<link rel="preload" as="fetch" crossorigin href="/api/report?company=google">"#,
            )
        );
        assert!(links("/", None).contains("/api/deck?company=google&amp;set=smart&amp;period=6m"));
    }
}
