//! Durable state in DuckDB: the attempt log, notes, daily scores, code drafts and submissions,
//! plus the judge's read-only test database attached alongside.
//!
//! Hot reads never come here: the server keeps the attempt log, card states and notes in
//! memory and only writes through. DuckDB earns its place on the analytical side (submission
//! history and statistics) and as a compact, compressed store for the test corpus.

use std::collections::{HashMap, HashSet};
use std::path::Path;

use anyhow::{Context, Result};
use duckdb::{Config, Connection, OptionalExt, params};
use openleet_proto::Expected;
use parking_lot::Mutex;
use serde::Serialize;
use serde_json::value::RawValue;

use openleet::model::{Attempt, Grade};

/// DuckDB's buffer pool; the whole box has 1 GB and the judge needs most of it.
const MEMORY_LIMIT: &str = "64MB";

const SCHEMA: &str = r"
CREATE TYPE IF NOT EXISTS grade AS ENUM ('again', 'good', 'less', 'skip');
CREATE TYPE IF NOT EXISTS verdict AS ENUM ('accepted', 'wrong_answer', 'time_limit_exceeded',
    'memory_limit_exceeded', 'runtime_error', 'compile_error', 'output_limit_exceeded',
    'internal_error');
CREATE SEQUENCE IF NOT EXISTS submission_id START 1;
CREATE TABLE IF NOT EXISTS attempts (
    slug VARCHAR NOT NULL,
    at_ms BIGINT NOT NULL,
    grade grade NOT NULL,
    guessed VARCHAR[] NOT NULL,
    score DOUBLE,
    hints UTINYINT NOT NULL
);
CREATE TABLE IF NOT EXISTS daily_scores (
    day DATE PRIMARY KEY,
    at_ms BIGINT NOT NULL,
    readiness DOUBLE NOT NULL,
    coverage DOUBLE NOT NULL,
    accuracy DOUBLE
);
CREATE TABLE IF NOT EXISTS notes (slug VARCHAR PRIMARY KEY, text VARCHAR NOT NULL, at_ms BIGINT NOT NULL);
-- Editor code per problem; an empty `code` means the starter. `previous` is what Reset replaced,
-- for Restore.
CREATE TABLE IF NOT EXISTS drafts (
    slug VARCHAR PRIMARY KEY,
    code VARCHAR NOT NULL,
    at_ms BIGINT NOT NULL,
    previous VARCHAR
);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS previous VARCHAR;
CREATE TABLE IF NOT EXISTS submissions (
    id BIGINT PRIMARY KEY DEFAULT nextval('submission_id'),
    slug VARCHAR NOT NULL,
    at_ms BIGINT NOT NULL,
    code VARCHAR NOT NULL,
    verdict verdict NOT NULL,
    passed USMALLINT NOT NULL,
    total USMALLINT NOT NULL,
    cpu_ms UINTEGER NOT NULL,
    -- What the result page shows (failing case, error); its shape depends on the verdict.
    detail VARIANT
);
";

/// Your code for a problem: the current draft and the version Reset replaced.
#[derive(Default, Serialize)]
pub struct Draft {
    pub code: Option<String>,
    pub previous: Option<String>,
}

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

/// One day's readiness, coverage and accuracy, for the progress chart.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct DailyScore {
    pub day: String,
    pub readiness: f64,
    pub coverage: f64,
    pub accuracy: Option<f64>,
}

/// The columns [`SubmissionRow::from_row`] reads, in order.
const SUBMISSION_COLUMNS: &str = "id, at_ms, verdict::VARCHAR, passed, total, cpu_ms";

/// A stored submission; `code` and `detail` only when one submission is read.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct SubmissionRow {
    pub id: i64,
    pub at: i64,
    pub verdict: String,
    pub passed: u16,
    pub total: u16,
    pub cpu_ms: u32,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub detail: Option<Box<RawValue>>,
}

impl SubmissionRow {
    /// A row's [`SUBMISSION_COLUMNS`], without code or detail.
    fn from_row(r: &duckdb::Row<'_>) -> duckdb::Result<Self> {
        Ok(Self {
            id: r.get(0)?,
            at: r.get(1)?,
            verdict: r.get(2)?,
            passed: r.get(3)?,
            total: r.get(4)?,
            cpu_ms: r.get(5)?,
            code: None,
            detail: None,
        })
    }
}

/// A finished submission, as stored.
pub struct NewSubmission<'a> {
    pub slug: &'a str,
    pub at: i64,
    pub code: &'a str,
    pub verdict: &'a str,
    pub passed: u16,
    pub total: u16,
    pub cpu_ms: u32,
    pub detail: &'a str,
}

/// Reads one problem's tests. Corpora built before digests existed have no
/// `expected_sha256` column.
const TESTS_QUERY: &str = "SELECT kind, test, expected, expected_sha256 FROM corpus.tests
    WHERE slug = ? ORDER BY idx";
const TESTS_QUERY_WITHOUT_DIGESTS: &str = "SELECT kind, test, expected, NULL::VARCHAR
    FROM corpus.tests WHERE slug = ? ORDER BY idx";

/// The progress database, with the test corpus attached when present.
pub struct Store {
    conn: Mutex<Connection>,
    /// The query for a problem's tests; `None` without a corpus.
    tests_query: Option<&'static str>,
}

impl Store {
    /// Opens (or creates) the progress database and attaches the test corpus read-only.
    pub fn open(path: &Path, tests: &Path) -> Result<Self> {
        if let Some(dir) = path.parent() {
            std::fs::create_dir_all(dir)?;
        }
        let config = Config::default()
            .max_memory(MEMORY_LIMIT)?
            .threads(1)?
            .enable_autoload_extension(false)?
            .with("checkpoint_threshold", "1MB")?;
        let conn = Connection::open_with_flags(path, config)
            .with_context(|| format!("opening {}", path.display()))?;
        conn.execute_batch(SCHEMA)?;
        let tests_query = if tests.exists() {
            conn.execute(
                &format!("ATTACH '{}' AS corpus (READ_ONLY)", tests.display()),
                [],
            )?;
            let digests: bool = conn.query_row(
                "SELECT count(*) > 0 FROM duckdb_columns()
                 WHERE database_name = 'corpus' AND table_name = 'tests'
                   AND column_name = 'expected_sha256'",
                [],
                |r| r.get(0),
            )?;
            Some(if digests {
                TESTS_QUERY
            } else {
                TESTS_QUERY_WITHOUT_DIGESTS
            })
        } else {
            None
        };
        Ok(Self {
            conn: Mutex::new(conn),
            tests_query,
        })
    }

    fn with<T>(&self, f: impl FnOnce(&Connection) -> duckdb::Result<T>) -> Result<T> {
        Ok(f(&self.conn.lock())?)
    }

    /// Copies the attempt log and notes of the old SQLite database once, when this one is new.
    pub fn import_sqlite(&self, sqlite: &Path) -> Result<usize> {
        if !sqlite.exists() || !self.attempts()?.is_empty() {
            return Ok(0);
        }
        let old = rusqlite::Connection::open_with_flags(
            sqlite,
            rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY,
        )?;
        let mut rows = old.prepare(
            "SELECT slug, at, grade, guessed, score, hints FROM attempts ORDER BY at, id",
        )?;
        let attempts = rows
            .query_map([], |r| {
                Ok((
                    r.get::<_, String>(0)?,
                    r.get::<_, i64>(1)?,
                    r.get::<_, String>(2)?,
                    r.get::<_, String>(3)?,
                    r.get::<_, Option<f64>>(4)?,
                    r.get::<_, i64>(5)?,
                ))
            })?
            .collect::<rusqlite::Result<Vec<_>>>()?;
        // Databases from before notes existed have no notes table.
        let notes = match old.prepare("SELECT slug, text, at FROM notes") {
            Ok(mut stmt) => stmt
                .query_map([], |r| {
                    Ok((
                        r.get::<_, String>(0)?,
                        r.get::<_, String>(1)?,
                        r.get::<_, i64>(2)?,
                    ))
                })?
                .collect::<rusqlite::Result<Vec<_>>>()?,
            Err(_) => Vec::new(),
        };
        self.with(|c| {
            let tx = c.unchecked_transaction()?;
            {
                let mut insert =
                    tx.prepare("INSERT INTO attempts VALUES (?, ?, ?, json(?)::VARCHAR[], ?, ?)")?;
                for (slug, at, grade, guessed, score, hints) in &attempts {
                    insert.execute(params![slug, at, grade, guessed, score, hints])?;
                }
                let mut insert = tx.prepare("INSERT OR REPLACE INTO notes VALUES (?, ?, ?)")?;
                for (slug, text, at) in &notes {
                    insert.execute(params![slug, text, at])?;
                }
            }
            tx.commit()
        })?;
        Ok(attempts.len())
    }

    /// The whole attempt log, oldest first.
    pub fn attempts(&self) -> Result<Vec<Attempt>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT slug, at_ms, grade::VARCHAR, to_json(guessed)::VARCHAR, score, hints
                 FROM attempts ORDER BY at_ms",
            )?;
            let rows = stmt.query_map([], |r| {
                let grade: String = r.get(2)?;
                let guessed: String = r.get(3)?;
                Ok(Attempt {
                    slug: r.get(0)?,
                    at: r.get(1)?,
                    grade: grade.parse().unwrap_or(Grade::Skip),
                    guessed: serde_json::from_str(&guessed).unwrap_or_default(),
                    score: r.get(4)?,
                    hints: r.get(5)?,
                })
            })?;
            rows.collect()
        })
    }

    /// Appends one attempt to the log.
    pub fn insert_attempt(&self, a: &Attempt) -> Result<()> {
        let guessed = serde_json::to_string(&a.guessed)?;
        self.with(|c| {
            c.prepare_cached("INSERT INTO attempts VALUES (?, ?, ?, json(?)::VARCHAR[], ?, ?)")?
                .execute(params![
                    a.slug,
                    a.at,
                    a.grade.as_str(),
                    guessed,
                    a.score,
                    a.hints
                ])
                .map(drop)
        })
    }

    /// Clears one problem's history, or every attempt and daily score.
    pub fn delete_attempts(&self, slug: Option<&str>) -> Result<()> {
        self.with(|c| match slug {
            Some(slug) => c
                .execute("DELETE FROM attempts WHERE slug = ?", [slug])
                .map(drop),
            None => c.execute_batch("DELETE FROM attempts; DELETE FROM daily_scores;"),
        })
    }

    /// Stores one day's scores, replacing that day's earlier ones.
    pub fn save_daily_score(&self, at: i64, s: &DailyScore) -> Result<()> {
        self.with(|c| {
            c.prepare_cached("INSERT OR REPLACE INTO daily_scores VALUES (?::DATE, ?, ?, ?, ?)")?
                .execute(params![s.day, at, s.readiness, s.coverage, s.accuracy])
                .map(drop)
        })
    }

    /// The last `limit` days with a score, oldest first.
    pub fn daily_scores(&self, limit: usize) -> Result<Vec<DailyScore>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT strftime(d, '%Y-%m-%d'), readiness, coverage, accuracy
                 FROM (FROM daily_scores SELECT day AS d, * ORDER BY day DESC LIMIT ?) ORDER BY d",
            )?;
            let rows = stmt.query_map([limit], |r| {
                Ok(DailyScore {
                    day: r.get(0)?,
                    readiness: r.get(1)?,
                    coverage: r.get(2)?,
                    accuracy: r.get(3)?,
                })
            })?;
            rows.collect()
        })
    }

    /// Every note, by slug.
    pub fn notes(&self) -> Result<HashMap<String, String>> {
        self.with(|c| {
            let mut stmt = c.prepare("SELECT slug, text FROM notes")?;
            let rows = stmt.query_map([], |r| Ok((r.get(0)?, r.get(1)?)))?;
            rows.collect()
        })
    }

    /// Saves your answer to a problem; empty text deletes it.
    pub fn save_note(&self, slug: &str, text: &str, at: i64) -> Result<()> {
        self.with(|c| {
            if text.is_empty() {
                c.prepare_cached("DELETE FROM notes WHERE slug = ?")?
                    .execute([slug])
                    .map(drop)
            } else {
                c.prepare_cached(
                    "MERGE INTO notes USING (SELECT ? AS slug, ? AS text, ? AS at_ms) AS new
                     USING (slug) WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT",
                )?
                .execute(params![slug, text, at])
                .map(drop)
            }
        })
    }

    /// Saves the editor's code ('' for "back to the starter"), keeping any previous version.
    pub fn save_draft(&self, slug: &str, code: &str, at: i64) -> Result<()> {
        self.with(|c| {
            c.prepare_cached(
                "MERGE INTO drafts USING (SELECT ? AS slug, ? AS code, ? AS at_ms) AS new
                 USING (slug)
                 WHEN MATCHED THEN UPDATE SET code = new.code, at_ms = new.at_ms
                 WHEN NOT MATCHED THEN INSERT (slug, code, at_ms) VALUES (new.slug, new.code, new.at_ms)",
            )?
            .execute(params![slug, code, at])?;
            // Nothing left to keep.
            c.prepare_cached("DELETE FROM drafts WHERE slug = ? AND code = '' AND previous IS NULL")?
                .execute([slug])
                .map(drop)
        })
    }

    /// A problem's draft; empty when there is none.
    pub fn draft(&self, slug: &str) -> Result<Draft> {
        let row = self.with(|c| {
            c.prepare_cached("SELECT nullif(code, ''), previous FROM drafts WHERE slug = ?")?
                .query_row([slug], |r| {
                    Ok(Draft {
                        code: r.get(0)?,
                        previous: r.get(1)?,
                    })
                })
                .optional()
        })?;
        Ok(row.unwrap_or_default())
    }

    /// Reset: the editor goes back to the starter and `current` becomes the previous version
    /// (an empty `current` keeps the previous version there was).
    pub fn reset_draft(&self, slug: &str, current: &str, at: i64) -> Result<Draft> {
        self.with(|c| {
            c.prepare_cached(
                "MERGE INTO drafts USING (SELECT ? AS slug, nullif(?, '') AS current, ? AS at_ms) AS new
                 USING (slug)
                 WHEN MATCHED THEN UPDATE SET code = '', at_ms = new.at_ms,
                     previous = coalesce(new.current, drafts.previous)
                 WHEN NOT MATCHED AND new.current IS NOT NULL THEN
                     INSERT (slug, code, at_ms, previous) VALUES (new.slug, '', new.at_ms, new.current)",
            )?
            .execute(params![slug, current, at])
            .map(drop)
        })?;
        self.draft(slug)
    }

    /// Restore: the previous version comes back and `current` becomes the previous one, so
    /// Restore again undoes it. `None` when there is nothing to restore.
    pub fn restore_draft(&self, slug: &str, current: &str, at: i64) -> Result<Option<Draft>> {
        if self.draft(slug)?.previous.is_none() {
            return Ok(None);
        }
        self.with(|c| {
            c.prepare_cached(
                "UPDATE drafts SET code = previous, previous = nullif(?, ''), at_ms = ?
                 WHERE slug = ?",
            )?
            .execute(params![current, at, slug])
            .map(drop)
        })?;
        self.draft(slug).map(Some)
    }

    /// A problem's tests in order. The corpus is sorted by slug, so zone maps skip every
    /// row group but the one or two that hold it.
    pub fn tests(&self, slug: &str) -> Result<Vec<TestRow>> {
        let Some(query) = self.tests_query else {
            return Ok(Vec::new());
        };
        let rows = self.with(|c| {
            let mut stmt = c.prepare_cached(query)?;
            let rows = stmt.query_map([slug], |r| {
                Ok((
                    r.get::<_, String>(0)?,
                    r.get::<_, String>(1)?,
                    r.get::<_, Option<String>>(2)?,
                    r.get::<_, Option<String>>(3)?,
                ))
            })?;
            rows.collect::<duckdb::Result<Vec<_>>>()
        })?;
        rows.into_iter()
            .enumerate()
            .map(|(idx, (kind, test, value, digest))| {
                let expected = match (value, digest) {
                    (_, Some(digest)) => Expected::Sha256(digest),
                    (Some(value), None) => Expected::Value(
                        RawValue::from_string(value)
                            .with_context(|| format!("expected output {idx} of {slug}"))?,
                    ),
                    (None, None) => anyhow::bail!("test {idx} of {slug} has no expected output"),
                };
                Ok(TestRow {
                    kind,
                    test,
                    expected,
                })
            })
            .collect()
    }

    /// Stores a judged submission and returns its id.
    pub fn insert_submission(&self, s: &NewSubmission) -> Result<i64> {
        self.with(|c| {
            c.prepare_cached(
                "INSERT INTO submissions (slug, at_ms, code, verdict, passed, total, cpu_ms, detail)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?::JSON::VARIANT) RETURNING id",
            )?
            .query_row(
                params![s.slug, s.at, s.code, s.verdict, s.passed, s.total, s.cpu_ms, s.detail],
                |r| r.get(0),
            )
        })
    }

    /// A problem's submissions, newest first, without code or detail.
    pub fn submissions(&self, slug: &str, limit: usize) -> Result<Vec<SubmissionRow>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(&format!(
                "SELECT {SUBMISSION_COLUMNS} FROM submissions WHERE slug = ? ORDER BY id DESC LIMIT ?"
            ))?;
            let rows = stmt.query_map(params![slug, limit], SubmissionRow::from_row)?;
            rows.collect()
        })
    }

    /// One submission with its code and result detail.
    pub fn submission(&self, id: i64) -> Result<Option<SubmissionRow>> {
        self.with(|c| {
            c.prepare_cached(&format!(
                "SELECT {SUBMISSION_COLUMNS}, code, detail::JSON::VARCHAR FROM submissions WHERE id = ?"
            ))?
            .query_row([id], |r| {
                let detail: Option<String> = r.get(7)?;
                Ok(SubmissionRow {
                    code: Some(r.get(6)?),
                    detail: detail.and_then(|d| RawValue::from_string(d).ok()),
                    ..SubmissionRow::from_row(r)?
                })
            })
            .optional()
        })
    }

    /// Problems with at least one accepted submission.
    pub fn solved(&self) -> Result<HashSet<String>> {
        self.with(|c| {
            let mut stmt =
                c.prepare("SELECT DISTINCT slug FROM submissions WHERE verdict = 'accepted'")?;
            let rows = stmt.query_map([], |r| r.get(0))?;
            rows.collect()
        })
    }

    /// Flushes the write-ahead log into the database file.
    pub fn checkpoint(&self) -> Result<()> {
        self.with(|c| c.execute_batch("CHECKPOINT"))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn store() -> (Store, std::path::PathBuf) {
        let dir = std::env::temp_dir().join(format!(
            "openleet-db-{}-{:?}",
            std::process::id(),
            std::thread::current().id()
        ));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        (
            Store::open(&dir.join("openleet.duckdb"), &dir.join("missing.duckdb")).unwrap(),
            dir,
        )
    }

    /// A store over a corpus with two tests of "a", made with or without the digest column.
    fn store_with_corpus(digests: bool) -> Store {
        let dir = std::env::temp_dir().join(format!(
            "openleet-corpus-{digests}-{}-{:?}",
            std::process::id(),
            std::thread::current().id()
        ));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        let corpus = dir.join("tests.duckdb");
        let c = Connection::open(&corpus).unwrap();
        if digests {
            c.execute_batch(
                "CREATE TABLE tests (slug VARCHAR, idx USMALLINT, kind VARCHAR, test VARCHAR,
                    expected VARCHAR, expected_sha256 VARCHAR);
                 INSERT INTO tests VALUES ('a', 1, 'stress', '{\"gen\":\"a\"}', NULL, 'ab12'),
                    ('a', 0, 'example', '{\"input\":{}}', '[1, 2]', NULL);",
            )
            .unwrap();
        } else {
            c.execute_batch(
                "CREATE TABLE tests (slug VARCHAR, idx USMALLINT, kind VARCHAR, test VARCHAR,
                    expected VARCHAR);
                 INSERT INTO tests VALUES ('a', 0, 'example', '{\"input\":{}}', '[1, 2]');",
            )
            .unwrap();
        }
        drop(c);
        Store::open(&dir.join("openleet.duckdb"), &corpus).unwrap()
    }

    #[test]
    fn reads_expected_values_and_digests() {
        let tests = store_with_corpus(true).tests("a").unwrap();
        assert_eq!(tests.len(), 2);
        assert!(matches!(&tests[0].expected, Expected::Value(v) if v.get() == "[1, 2]"));
        assert!(matches!(&tests[1].expected, Expected::Sha256(d) if d == "ab12"));
        let old = store_with_corpus(false).tests("a").unwrap();
        assert!(matches!(&old[0].expected, Expected::Value(v) if v.get() == "[1, 2]"));
        assert_eq!(store_with_corpus(false).tests("b").unwrap().len(), 0);
    }

    fn attempt(slug: &str, at: i64, grade: Grade) -> Attempt {
        Attempt {
            slug: slug.into(),
            at,
            grade,
            guessed: vec!["Array".into(), "Hash Table".into()],
            score: Some(0.5),
            hints: 1,
        }
    }

    #[test]
    fn attempts_round_trip_in_order() {
        let (store, _dir) = store();
        store.insert_attempt(&attempt("b", 2, Grade::Good)).unwrap();
        store
            .insert_attempt(&attempt("a", 1, Grade::Again))
            .unwrap();
        let all = store.attempts().unwrap();
        assert_eq!(
            all.iter().map(|a| a.slug.as_str()).collect::<Vec<_>>(),
            ["a", "b"]
        );
        assert_eq!(all[0].grade, Grade::Again);
        assert_eq!(all[0].guessed, ["Array", "Hash Table"]);
        store.delete_attempts(Some("a")).unwrap();
        assert_eq!(store.attempts().unwrap().len(), 1);
        store.delete_attempts(None).unwrap();
        assert_eq!(store.attempts().unwrap().len(), 0);
    }

    #[test]
    fn notes_and_drafts_upsert_and_delete() {
        let (store, _dir) = store();
        store.save_note("a", "first", 1).unwrap();
        store.save_note("a", "second", 2).unwrap();
        assert_eq!(
            store.notes().unwrap().get("a").map(String::as_str),
            Some("second")
        );
        store.save_note("a", "", 3).unwrap();
        assert!(store.notes().unwrap().is_empty());
        store.save_draft("a", "code 1", 1).unwrap();
        store.save_draft("a", "code 2", 2).unwrap();
        assert_eq!(store.draft("a").unwrap().code.as_deref(), Some("code 2"));
        store.save_draft("a", "", 3).unwrap();
        assert_eq!(store.draft("a").unwrap().code, None);
    }

    #[test]
    fn reset_and_restore_swap_versions() {
        let (store, _dir) = store();
        // Reset with nothing saved yet still keeps what was in the editor.
        let reset = store.reset_draft("a", "mine", 1).unwrap();
        assert_eq!(
            (reset.code, reset.previous.as_deref()),
            (None, Some("mine"))
        );
        store.save_draft("a", "new try", 2).unwrap();
        let restored = store.restore_draft("a", "new try", 3).unwrap().unwrap();
        assert_eq!(restored.code.as_deref(), Some("mine"));
        assert_eq!(restored.previous.as_deref(), Some("new try"));
        // Restoring again swaps back.
        let again = store.restore_draft("a", "mine", 4).unwrap().unwrap();
        assert_eq!(again.code.as_deref(), Some("new try"));
        // Reset of an empty editor keeps the earlier previous version.
        store.reset_draft("a", "", 5).unwrap();
        assert_eq!(store.draft("a").unwrap().previous.as_deref(), Some("mine"));
        assert!(store.restore_draft("b", "x", 6).unwrap().is_none());
    }

    #[test]
    fn daily_scores_keep_one_row_per_day() {
        let (store, _dir) = store();
        let daily = |day: &str, r| DailyScore {
            day: day.to_owned(),
            readiness: r,
            coverage: 0.1,
            accuracy: None,
        };
        store
            .save_daily_score(1, &daily("2026-11-01", 0.1))
            .unwrap();
        store
            .save_daily_score(2, &daily("2026-11-02", 0.2))
            .unwrap();
        store
            .save_daily_score(3, &daily("2026-11-02", 0.3))
            .unwrap();
        let days = store.daily_scores(60).unwrap();
        assert_eq!(
            days.iter().map(|d| d.day.as_str()).collect::<Vec<_>>(),
            ["2026-11-01", "2026-11-02"]
        );
        assert!((days[1].readiness - 0.3).abs() < 1e-9);
        assert_eq!(store.daily_scores(1).unwrap()[0].day, "2026-11-02");
    }

    #[test]
    fn submissions_store_variant_detail() {
        let (store, _dir) = store();
        let new = |verdict| NewSubmission {
            slug: "a",
            at: 5,
            code: "print(1)",
            verdict,
            passed: 3,
            total: 9,
            cpu_ms: 40,
            detail: r#"{"failing":{"input":"x = 1","kind":"hidden"},"limitMs":2000}"#,
        };
        let first = store.insert_submission(&new("wrong_answer")).unwrap();
        let second = store.insert_submission(&new("accepted")).unwrap();
        assert!(second > first);
        let list = store.submissions("a", 10).unwrap();
        assert_eq!(
            list.iter().map(|s| s.id).collect::<Vec<_>>(),
            [second, first]
        );
        let one = store.submission(first).unwrap().unwrap();
        assert_eq!(one.code.as_deref(), Some("print(1)"));
        let detail: serde_json::Value = serde_json::from_str(one.detail.unwrap().get()).unwrap();
        assert_eq!(detail["failing"]["kind"], "hidden");
        assert_eq!(store.solved().unwrap(), HashSet::from(["a".to_owned()]));
    }

    #[test]
    fn imports_old_sqlite_once() {
        let (store, dir) = store();
        let path = dir.join("progress.db");
        let old = rusqlite::Connection::open(&path).unwrap();
        old.execute_batch(
            "CREATE TABLE attempts (id INTEGER PRIMARY KEY, slug TEXT, at INTEGER, grade TEXT,
                guessed TEXT, score REAL, hints INTEGER);
             INSERT INTO attempts (slug, at, grade, guessed, score, hints)
                VALUES ('two-sum', 10, 'good', '[\"Array\"]', 1.0, 0);",
        )
        .unwrap();
        drop(old);
        assert_eq!(store.import_sqlite(&path).unwrap(), 1);
        assert_eq!(store.import_sqlite(&path).unwrap(), 0);
        assert_eq!(store.attempts().unwrap()[0].guessed, ["Array"]);
    }
}
