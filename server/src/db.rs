//! Durable state in DuckDB: the attempt log, notes, daily scores, code drafts and submissions,
//! plus the judge's read-only test database attached alongside.
//!
//! Hot reads never come here: the server keeps the attempt log, card states and notes in
//! memory and only writes through. DuckDB earns its place on the analytical side (submission
//! history and statistics) and as a compact, compressed store for the test corpus.

use std::collections::HashMap;
use std::path::Path;

use anyhow::{Context, Result};
use duckdb::{Config, Connection, OptionalExt, params};
use parking_lot::Mutex;
use serde::Serialize;

use cards::model::{Attempt, Grade};

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
CREATE TABLE IF NOT EXISTS drafts (slug VARCHAR PRIMARY KEY, code VARCHAR NOT NULL, at_ms BIGINT NOT NULL);
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

/// One stored test of the judge's corpus.
pub struct TestRow {
    pub kind: String,
    /// The test as the zygote takes it: `{"input": ...}` or a generator reference.
    pub test: String,
    pub expected: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct DailyScore {
    pub day: String,
    pub readiness: f64,
    pub coverage: f64,
    pub accuracy: Option<f64>,
}

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
    pub detail: Option<Box<serde_json::value::RawValue>>,
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

pub struct Store {
    conn: Mutex<Connection>,
    has_tests: bool,
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
        let has_tests = tests.exists();
        if has_tests {
            conn.execute(
                &format!("ATTACH '{}' AS corpus (READ_ONLY)", tests.display()),
                [],
            )?;
        }
        Ok(Self {
            conn: Mutex::new(conn),
            has_tests,
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

    pub fn save_daily_score(&self, day: &str, at: i64, s: &DailyScore) -> Result<()> {
        self.with(|c| {
            c.prepare_cached("INSERT OR REPLACE INTO daily_scores VALUES (?::DATE, ?, ?, ?, ?)")?
                .execute(params![day, at, s.readiness, s.coverage, s.accuracy])
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

    pub fn notes(&self) -> Result<HashMap<String, String>> {
        self.with(|c| {
            let mut stmt = c.prepare("SELECT slug, text FROM notes")?;
            let rows = stmt.query_map([], |r| Ok((r.get(0)?, r.get(1)?)))?;
            rows.collect()
        })
    }

    /// Upserts a text row keyed by slug (notes, drafts); empty text deletes it.
    fn save_text(&self, table: Table, slug: &str, text: &str, at: i64) -> Result<()> {
        let (delete, merge) = table.statements();
        self.with(|c| {
            if text.is_empty() {
                c.prepare_cached(delete)?.execute([slug]).map(drop)
            } else {
                c.prepare_cached(merge)?
                    .execute(params![slug, text, at])
                    .map(drop)
            }
        })
    }

    pub fn save_note(&self, slug: &str, text: &str, at: i64) -> Result<()> {
        self.save_text(Table::Notes, slug, text, at)
    }

    pub fn save_draft(&self, slug: &str, code: &str, at: i64) -> Result<()> {
        self.save_text(Table::Drafts, slug, code, at)
    }

    pub fn draft(&self, slug: &str) -> Result<Option<String>> {
        self.with(|c| {
            c.prepare_cached("SELECT code FROM drafts WHERE slug = ?")?
                .query_row([slug], |r| r.get(0))
                .optional()
        })
    }

    /// A problem's tests in order. The corpus is sorted by slug, so zone maps skip every
    /// row group but the one or two that hold it.
    pub fn tests(&self, slug: &str) -> Result<Vec<TestRow>> {
        if !self.has_tests {
            return Ok(Vec::new());
        }
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT kind, test, expected FROM corpus.tests WHERE slug = ? ORDER BY idx",
            )?;
            let rows = stmt.query_map([slug], |r| {
                Ok(TestRow {
                    kind: r.get(0)?,
                    test: r.get(1)?,
                    expected: r.get(2)?,
                })
            })?;
            rows.collect()
        })
    }

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

    /// A problem's submissions, newest first.
    pub fn submissions(&self, slug: &str, limit: usize) -> Result<Vec<SubmissionRow>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT id, at_ms, verdict::VARCHAR, passed, total, cpu_ms FROM submissions
                 WHERE slug = ? ORDER BY id DESC LIMIT ?",
            )?;
            let rows = stmt.query_map(params![slug, limit], |r| {
                Ok(SubmissionRow {
                    id: r.get(0)?,
                    at: r.get(1)?,
                    verdict: r.get(2)?,
                    passed: r.get(3)?,
                    total: r.get(4)?,
                    cpu_ms: r.get(5)?,
                    code: None,
                    detail: None,
                })
            })?;
            rows.collect()
        })
    }

    pub fn submission(&self, id: i64) -> Result<Option<SubmissionRow>> {
        let row = self.with(|c| {
            c.prepare_cached(
                "SELECT id, at_ms, verdict::VARCHAR, passed, total, cpu_ms, code,
                        detail::JSON::VARCHAR FROM submissions WHERE id = ?",
            )?
            .query_row([id], |r| {
                Ok((
                    SubmissionRow {
                        id: r.get(0)?,
                        at: r.get(1)?,
                        verdict: r.get(2)?,
                        passed: r.get(3)?,
                        total: r.get(4)?,
                        cpu_ms: r.get(5)?,
                        code: Some(r.get(6)?),
                        detail: None,
                    },
                    r.get::<_, Option<String>>(7)?,
                ))
            })
            .optional()
        })?;
        Ok(row.map(|(mut sub, detail)| {
            sub.detail = detail.and_then(|d| serde_json::value::RawValue::from_string(d).ok());
            sub
        }))
    }

    /// Problems with at least one accepted submission.
    pub fn solved(&self) -> Result<Vec<String>> {
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

#[derive(Clone, Copy)]
enum Table {
    Notes,
    Drafts,
}

impl Table {
    /// (delete, upsert) statements; MERGE keeps one row per slug.
    const fn statements(self) -> (&'static str, &'static str) {
        match self {
            Self::Notes => (
                "DELETE FROM notes WHERE slug = ?",
                "MERGE INTO notes USING (SELECT ? AS slug, ? AS text, ? AS at_ms) AS new
                 USING (slug) WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT",
            ),
            Self::Drafts => (
                "DELETE FROM drafts WHERE slug = ?",
                "MERGE INTO drafts USING (SELECT ? AS slug, ? AS code, ? AS at_ms) AS new
                 USING (slug) WHEN MATCHED THEN UPDATE WHEN NOT MATCHED THEN INSERT",
            ),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn store() -> (Store, std::path::PathBuf) {
        let dir = std::env::temp_dir().join(format!(
            "cards-db-{}-{:?}",
            std::process::id(),
            std::thread::current().id()
        ));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        (
            Store::open(&dir.join("cards.duckdb"), &dir.join("missing.duckdb")).unwrap(),
            dir,
        )
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
        assert!(store.attempts().unwrap().is_empty());
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
        assert_eq!(store.draft("a").unwrap().as_deref(), Some("code 2"));
        store.save_draft("a", "", 3).unwrap();
        assert_eq!(store.draft("a").unwrap(), None);
    }

    #[test]
    fn daily_scores_keep_one_row_per_day() {
        let (store, _dir) = store();
        let score = |r| DailyScore {
            day: String::new(),
            readiness: r,
            coverage: 0.1,
            accuracy: None,
        };
        store
            .save_daily_score("2026-11-01", 1, &score(0.1))
            .unwrap();
        store
            .save_daily_score("2026-11-02", 2, &score(0.2))
            .unwrap();
        store
            .save_daily_score("2026-11-02", 3, &score(0.3))
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
        assert_eq!(store.solved().unwrap(), ["a"]);
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
