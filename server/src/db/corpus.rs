//! The judge's test corpus (`data/judge/tests.duckdb`, built by
//! `src/openleet/judging/assemble.py`), attached read-only to the progress database as `corpus`.
//!
//! Schema 1 has a one-row `meta` table naming its version; corpora built before it (schema 0,
//! still the published one until the next rebuild) have only `tests`, with the old column
//! names. Any other version is refused: the server then runs without tests rather than
//! misreading them.

use std::path::Path;

use anyhow::{Context, Result, bail};
use duckdb::Connection;
use openleet_proto::Expected;
use serde_json::value::RawValue;

use super::sql_string;

/// The corpus schema this build reads (besides schema 0).
pub const SCHEMA_VERSION: u16 = 1;

/// A problem's tests, in order: kind, test, expected value (JSON text), expected digest.
const TESTS_QUERY: &str =
    "SELECT kind::VARCHAR, test_case::VARCHAR, expected::VARCHAR, expected_sha256
    FROM corpus.tests WHERE slug = ? ORDER BY idx";
const TESTS_QUERY_V0: &str = "SELECT kind, test, expected, expected_sha256
    FROM corpus.tests WHERE slug = ? ORDER BY idx";

/// One stored test of the judge's corpus.
pub struct TestRow {
    pub kind: String,
    /// The test as the zygote takes it: `{"input": ...}` or a generator reference.
    pub test: String,
    pub expected: Expected,
}

impl TestRow {
    /// Whether the test is one of the problem's examples (shown and used by Run).
    pub fn is_example(&self) -> bool {
        self.kind == "example"
    }
}

/// An attached corpus that passed its checks.
pub struct Corpus {
    query: &'static str,
}

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
        Ok((query, summary)) => {
            tracing::info!("test corpus {}: {summary}", path.display());
            Ok(Some(Corpus { query }))
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

/// The tests query for the attached corpus's schema, and a summary to log.
fn check(conn: &Connection) -> Result<(&'static str, String)> {
    let has = |table: &str, column: &str| -> duckdb::Result<bool> {
        conn.query_row(
            "SELECT count(*) > 0 FROM duckdb_columns()
             WHERE database_name = 'corpus' AND table_name = ? AND column_name = ?",
            [table, column],
            |r| r.get(0),
        )
    };
    if !has("meta", "schema_version")? {
        if has("tests", "expected_sha256")? {
            let tests: i64 =
                conn.query_row("SELECT count(*) FROM corpus.tests", [], |r| r.get(0))?;
            return Ok((
                TESTS_QUERY_V0,
                format!("schema 0 (no meta table), {tests} tests"),
            ));
        }
        bail!("no meta table and not the schema 0 layout");
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
        bail!("schema version {version}, this build reads {SCHEMA_VERSION} (and 0)");
    }
    if tests != actual {
        bail!("meta counts {tests} tests but the table holds {actual}");
    }
    let built_at = jiff::Timestamp::from_millisecond(built_ms)?;
    Ok((
        TESTS_QUERY,
        format!("schema {version}, built {built_at}, {tests} tests of {problems} problems"),
    ))
}

impl Corpus {
    /// A problem's tests in order. The corpus is sorted by slug, so zone maps skip every row
    /// group but the one or two that hold it.
    pub fn tests(&self, conn: &Connection, slug: &str) -> Result<Vec<TestRow>> {
        let mut stmt = conn.prepare_cached(self.query)?;
        let rows = stmt
            .query_map([slug], |r| {
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

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    /// A corpus with tests of "a" (a stress test stored first, to check the ordering).
    const V1: &str = r#"
        CREATE TYPE test_kind AS ENUM ('example', 'hidden', 'stress');
        CREATE TABLE tests (slug VARCHAR NOT NULL, idx USMALLINT NOT NULL,
            kind test_kind NOT NULL, test_case JSON NOT NULL, expected JSON,
            expected_sha256 VARCHAR, PRIMARY KEY (slug, idx));
        INSERT INTO tests VALUES ('a', 1, 'stress', '{"gen":"a"}', NULL, 'ab12'),
            ('a', 0, 'example', '{"input":{}}', '[1, 2]', NULL);
        CREATE TABLE meta (schema_version USMALLINT NOT NULL, built_at TIMESTAMPTZ NOT NULL,
            built_by VARCHAR NOT NULL, problem_count UINTEGER NOT NULL,
            test_count UINTEGER NOT NULL);
    "#;
    const V0: &str = r#"
        CREATE TABLE tests (slug VARCHAR, idx USMALLINT, kind VARCHAR, test VARCHAR,
            expected VARCHAR, expected_sha256 VARCHAR);
        INSERT INTO tests VALUES ('a', 1, 'stress', '{"gen":"a"}', NULL, 'ab12'),
            ('a', 0, 'example', '{"input":{}}', '[1, 2]', NULL);
    "#;

    fn attached(dir: &TempDir, ddl: &str) -> (Connection, Option<Corpus>) {
        let path = dir.path("tests.duckdb");
        Connection::open(&path).unwrap().execute_batch(ddl).unwrap();
        let conn = Connection::open_in_memory().unwrap();
        let corpus = attach(&conn, &path).unwrap();
        (conn, corpus)
    }

    fn assert_reads_both_kinds(conn: &Connection, corpus: &Corpus) {
        let tests = corpus.tests(conn, "a").unwrap();
        assert_eq!(tests.len(), 2);
        assert!(tests[0].is_example());
        assert_eq!(tests[0].test, r#"{"input":{}}"#);
        assert!(matches!(&tests[0].expected, Expected::Value(v) if v.get() == "[1, 2]"));
        assert!(matches!(&tests[1].expected, Expected::Sha256(d) if d == "ab12"));
        assert!(corpus.tests(conn, "b").unwrap().is_empty());
    }

    #[test]
    fn reads_schema_1() {
        let dir = TempDir::new("corpus-v1");
        let meta = "INSERT INTO meta VALUES (1, now(), 'test', 1, 2);";
        let (conn, corpus) = attached(&dir, &format!("{V1}{meta}"));
        assert_reads_both_kinds(&conn, &corpus.expect("accepted"));
    }

    #[test]
    fn reads_schema_0() {
        let dir = TempDir::new("corpus-v0");
        let (conn, corpus) = attached(&dir, V0);
        assert_reads_both_kinds(&conn, &corpus.expect("accepted"));
    }

    #[test]
    fn refuses_unknown_versions_and_bad_counts() {
        for meta in [
            "INSERT INTO meta VALUES (2, now(), 'test', 1, 2);",
            "INSERT INTO meta VALUES (1, now(), 'test', 1, 3);",
            "",
        ] {
            let dir = TempDir::new("corpus-refused");
            let (conn, corpus) = attached(&dir, &format!("{V1}{meta}"));
            assert!(corpus.is_none(), "{meta}");
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
