//! The judge's test corpus (`data/judge/tests.duckdb`, built by
//! `src/openleet/judging/assemble.py`), attached read-only to the progress database as `corpus`.
//!
//! A one-row `meta` table names the corpus's schema version. A corpus of any other version than
//! [`SCHEMA_VERSION`] is refused: the server then runs without tests rather than misreading
//! them.

use std::path::Path;

use anyhow::{Context, Result, bail};
use duckdb::Connection;
use openleet_proto::Expected;
use serde_json::value::RawValue;

use super::sql_string;

/// The corpus schema this build reads.
pub const SCHEMA_VERSION: u16 = 1;

/// A problem's tests (all of them, or only the examples when `$2`), in order: kind, test,
/// expected value (JSON text), expected digest.
const TESTS_QUERY: &str =
    "SELECT kind::VARCHAR, test_case::VARCHAR, expected::VARCHAR, expected_sha256
    FROM corpus.tests WHERE slug = $1 AND (NOT $2 OR kind = 'example') ORDER BY idx";

/// One stored test of the judge's corpus.
pub struct TestRow {
    pub kind: String,
    /// The test as the zygote takes it: `{"input": ...}` or a generator reference.
    pub test: String,
    pub expected: Expected,
}

/// Which of a problem's tests to read.
#[derive(Clone, Copy)]
pub enum Tests {
    All,
    /// The examples, shown above the editor and used by Run.
    Examples,
}

/// An attached corpus that passed its checks.
pub struct Corpus;

/// Attaches the corpus at `path` read-only and checks it. `None` when there is no file or the
/// corpus is refused (logged); an error only when attaching itself fails.
pub fn attach(conn: &Connection, path: &Path) -> Result<Option<Corpus>> {
    if !path.exists() {
        tracing::warn!(
            "no test corpus at {}; nothing can be judged",
            path.display()
        );
        return Ok(None);
    }
    conn.execute_batch(&format!(
        "ATTACH {} AS corpus (READ_ONLY)",
        sql_string(path)
    ))
    .with_context(|| format!("attaching {}", path.display()))?;
    match check(conn) {
        Ok(summary) => {
            tracing::info!("test corpus {}: {summary}", path.display());
            Ok(Some(Corpus))
        }
        Err(error) => {
            tracing::error!(
                "refusing the test corpus {}: {error:#}; nothing can be judged",
                path.display()
            );
            conn.execute_batch("DETACH corpus")?;
            Ok(None)
        }
    }
}

/// Checks the attached corpus's schema version and counts; a summary to log.
fn check(conn: &Connection) -> Result<String> {
    let has_meta: bool = conn.query_row(
        "SELECT count(*) > 0 FROM duckdb_columns()
         WHERE database_name = 'corpus' AND table_name = 'meta' AND column_name = 'schema_version'",
        [],
        |r| r.get(0),
    )?;
    if !has_meta {
        bail!("no meta table");
    }
    let (rows, version, built_ms, problems, tests, actual): (i64, u16, i64, i64, i64, i64) = conn
        .query_row(
        "SELECT count(*), any_value(schema_version), any_value(epoch_ms(built_at)),
                any_value(problem_count), any_value(test_count),
                (SELECT count(*) FROM corpus.tests)
             FROM corpus.meta",
        [],
        |r| {
            Ok((
                r.get(0)?,
                r.get(1)?,
                r.get(2)?,
                r.get(3)?,
                r.get(4)?,
                r.get(5)?,
            ))
        },
    )?;
    if rows != 1 {
        bail!("meta has {rows} rows, expected 1");
    }
    if version != SCHEMA_VERSION {
        bail!("schema version {version}, this build reads {SCHEMA_VERSION}");
    }
    if tests != actual {
        bail!("meta counts {tests} tests but the table holds {actual}");
    }
    let built_at = jiff::Timestamp::from_millisecond(built_ms)?;
    Ok(format!(
        "schema {version}, built {built_at}, {tests} tests of {problems} problems"
    ))
}

impl Corpus {
    /// A problem's tests in order. The corpus is sorted by slug, so zone maps skip the row
    /// groups whose slug range does not hold it; the corpus has two, so a lookup scans about
    /// half of the slug column.
    pub fn tests(&self, conn: &Connection, slug: &str, which: Tests) -> Result<Vec<TestRow>> {
        let examples_only = matches!(which, Tests::Examples);
        let mut stmt = conn.prepare_cached(TESTS_QUERY)?;
        let rows = stmt
            .query_map(duckdb::params![slug, examples_only], |r| {
                Ok((
                    r.get::<_, String>(0)?,
                    r.get::<_, String>(1)?,
                    r.get::<_, Option<String>>(2)?,
                    r.get::<_, Option<String>>(3)?,
                ))
            })?
            .collect::<duckdb::Result<Vec<_>>>()?;
        rows.into_iter()
            .enumerate()
            .map(|(idx, (kind, test, value, digest))| {
                let expected = match (value, digest) {
                    (_, Some(digest)) => Expected::Sha256(digest),
                    (Some(value), None) => Expected::Value(
                        RawValue::from_string(value)
                            .with_context(|| format!("expected output {idx} of {slug}"))?,
                    ),
                    (None, None) => bail!("test {idx} of {slug} has no expected output"),
                };
                Ok(TestRow {
                    kind,
                    test,
                    expected,
                })
            })
            .collect()
    }
}

/// A schema 1 corpus with tests of "a" (stored out of order, to check the ordering), for
/// tests; [`SAMPLE_META`] completes it.
#[cfg(test)]
pub const SAMPLE: &str = r#"
    CREATE TYPE test_kind AS ENUM ('example', 'hidden', 'stress');
    CREATE TABLE tests (slug VARCHAR NOT NULL, idx USMALLINT NOT NULL,
        kind test_kind NOT NULL, test_case JSON NOT NULL, expected JSON,
        expected_sha256 VARCHAR, PRIMARY KEY (slug, idx));
    INSERT INTO tests VALUES ('a', 2, 'stress', '{"gen":"a"}', NULL, 'ab12'),
        ('a', 0, 'example', '{"input":{}}', '[1, 2]', NULL),
        ('a', 1, 'hidden', '{"input":{"n":3}}', '3', NULL);
    CREATE TABLE meta (schema_version USMALLINT NOT NULL, built_at TIMESTAMPTZ NOT NULL,
        built_by VARCHAR NOT NULL, problem_count UINTEGER NOT NULL,
        test_count UINTEGER NOT NULL);
"#;

/// The meta row that makes [`SAMPLE`] a valid corpus.
#[cfg(test)]
pub const SAMPLE_META: &str = "INSERT INTO meta VALUES (1, now(), 'test', 1, 3);";

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    fn attached(dir: &TempDir, ddl: &str) -> (Connection, Option<Corpus>) {
        let path = dir.path("tests.duckdb");
        Connection::open(&path).unwrap().execute_batch(ddl).unwrap();
        let conn = Connection::open_in_memory().unwrap();
        let corpus = attach(&conn, &path).unwrap();
        (conn, corpus)
    }

    #[test]
    fn reads_all_tests_or_only_the_examples() {
        let dir = TempDir::new("corpus-v1");
        let (conn, corpus) = attached(&dir, &format!("{SAMPLE}{SAMPLE_META}"));
        let corpus = corpus.expect("accepted");
        let tests = corpus.tests(&conn, "a", Tests::All).unwrap();
        assert_eq!(
            tests.iter().map(|t| t.kind.as_str()).collect::<Vec<_>>(),
            ["example", "hidden", "stress"]
        );
        assert_eq!(tests[0].test, r#"{"input":{}}"#);
        assert!(matches!(&tests[0].expected, Expected::Value(v) if v.get() == "[1, 2]"));
        assert!(matches!(&tests[2].expected, Expected::Sha256(d) if d == "ab12"));
        let examples = corpus.tests(&conn, "a", Tests::Examples).unwrap();
        assert_eq!(examples.len(), 1);
        assert_eq!(examples[0].test, tests[0].test);
        assert!(corpus.tests(&conn, "b", Tests::All).unwrap().is_empty());
    }

    #[test]
    fn refuses_unknown_versions_bad_counts_and_no_meta() {
        let no_meta = SAMPLE.replace("CREATE TABLE meta", "CREATE TABLE other");
        for ddl in [
            format!("{SAMPLE}INSERT INTO meta VALUES (2, now(), 'test', 1, 3);"),
            format!("{SAMPLE}INSERT INTO meta VALUES (1, now(), 'test', 1, 4);"),
            SAMPLE.to_owned(),
            no_meta,
        ] {
            let dir = TempDir::new("corpus-refused");
            let (conn, corpus) = attached(&dir, &ddl);
            assert!(corpus.is_none(), "{ddl}");
            // Refused corpora are detached again.
            assert!(conn.execute_batch("SELECT 1 FROM corpus.tests").is_err());
        }
    }

    #[test]
    fn a_missing_corpus_is_no_corpus() {
        let dir = TempDir::new("corpus-missing");
        let conn = Connection::open_in_memory().unwrap();
        assert!(attach(&conn, &dir.path("none.duckdb")).unwrap().is_none());
    }
}
