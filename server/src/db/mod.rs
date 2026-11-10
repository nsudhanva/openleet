//! Durable state in DuckDB: the attempt log, notes, daily scores, code drafts, submissions and
//! practice plans (`STATE_DIR/openleet.duckdb`, schema in `migrations/`), plus the judge's
//! read-only test corpus attached alongside.
//!
//! Hot reads never come here: the server keeps the attempt log, card states and notes in
//! memory and only writes through. DuckDB earns its place on the analytical side (submission
//! history and statistics) and as a compact, compressed store for the test corpus.
//!
//! The API speaks Unix milliseconds; the tables hold TIMESTAMPTZ. Every query converts at the
//! boundary: `to_timestamp(? / 1000)` in, `epoch_ms(column)` out (exact, and independent of
//! any time zone; see `migrations/0001_progress.sql`).

pub mod backup;
mod corpus;
pub mod migrate;
mod plans;
mod sqlite;

use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::time::Duration;

use anyhow::{Context, Result};
use duckdb::{Config, Connection, OptionalExt, params};
use jiff::civil::Date;
use parking_lot::Mutex;
use serde::Serialize;
use serde_json::value::RawValue;

use openleet::coding::{CodingLog, verdict_named};
use openleet::model::{Attempt, Grade};

pub use backup::Backup;
use corpus::Corpus;
pub use corpus::TestRow;
use migrate::{Migrated, Shape};
pub use plans::{Changed, MAX_PINNED_PLANS, PlanChange, PlanKey, SavedPlan};
pub use sqlite::Imported;

/// DuckDB's buffer pool; the whole box has 1 GB and the judge needs most of it.
const MEMORY_LIMIT: &str = "64MB";
/// Submissions kept per problem (each holds up to 64 KB of code).
pub const SUBMISSIONS_KEPT: usize = 100;

/// Your code for a problem: the current draft and the version Reset replaced.
#[derive(Default, Serialize)]
pub struct Draft {
    pub code: Option<String>,
    pub previous: Option<String>,
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
const SUBMISSION_COLUMNS: &str =
    "id, epoch_ms(submitted_at), verdict::VARCHAR, tests_passed, tests_total, cpu_ms";

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

/// How [`Store::open`] found the progress database.
#[derive(Debug)]
pub enum Opening {
    /// There was none; a new, empty one was created.
    Created,
    /// The existing one, migrated if it was behind.
    Existing(Migrated),
    /// It could not be opened: its files were moved to `quarantined` and the
    /// newest usable backup restored, or an empty database created when there was none.
    Recovered {
        quarantined: PathBuf,
        backup: Option<PathBuf>,
    },
}

impl Opening {
    /// Whether the database started out empty (so older data may be imported into it).
    pub fn started_empty(&self) -> bool {
        matches!(self, Self::Created | Self::Recovered { backup: None, .. })
    }
}

/// The progress database, with the test corpus attached when present.
pub struct Store {
    conn: Mutex<Connection>,
    corpus: Option<Corpus>,
    backups: PathBuf,
}

/// A path as a SQL string literal.
fn sql_string(path: &Path) -> String {
    format!("'{}'", path.to_string_lossy().replace('\'', "''"))
}

/// The current UTC time, for file names: `20261109T183000Z`.
fn stamp() -> String {
    jiff::Timestamp::now()
        .strftime("%Y%m%dT%H%M%SZ")
        .to_string()
}

/// Opens a database file with the server's settings.
fn connect(path: &Path) -> Result<Connection> {
    let config = Config::default()
        .max_memory(MEMORY_LIMIT)?
        .threads(1)?
        .enable_autoload_extension(false)?
        .with("checkpoint_threshold", "1MB")?;
    Connection::open_with_flags(path, config).with_context(|| format!("opening {}", path.display()))
}

/// An openable database must survive a failed backup or schema change in place.
#[derive(Debug, thiserror::Error)]
#[error("preparing the database failed; leaving its files in place")]
struct SetupFailed;

/// Opens and migrates the database at `path`, first copying it aside when a migration is due
/// (see [`backup::before_migrating`]).
fn open_and_migrate(path: &Path, backups: &Path) -> Result<(Connection, Opening)> {
    let mut conn = connect(path)?;
    let opening = prepare_database(&mut conn, backups).context(SetupFailed)?;
    Ok((conn, opening))
}

fn prepare_database(conn: &mut Connection, backups: &Path) -> Result<Opening> {
    let behind = match migrate::shape(conn)? {
        Shape::Empty => false,
        Shape::Unversioned => true,
        Shape::Version(v) => v < migrate::latest(),
    };
    if behind {
        let copy = backup::before_migrating(conn, backups, &stamp())?;
        tracing::info!(
            "migrating the progress database; a copy is kept at {}",
            copy.display()
        );
    }
    let migrated = migrate::migrate(conn)?;
    if migrated.changed() {
        tracing::info!(
            "progress database migrated from {:?} to version {}",
            migrated.from,
            migrated.to
        );
    }
    let opening = if migrated.from == Shape::Empty {
        Opening::Created
    } else {
        Opening::Existing(migrated)
    };
    Ok(opening)
}

/// Whether a failure to open the database at `path` means the file itself is bad (so
/// recovering from a backup is right): not this build being too old for it, not another
/// process holding it, and not a problem any database would have (settings, disk, memory),
/// which a new scratch database next to it would hit too.
fn recoverable(error: &anyhow::Error, path: &Path) -> bool {
    if error.downcast_ref::<SetupFailed>().is_some()
        || format!("{error:#}").contains("Could not set lock")
    {
        return false;
    }
    let probe = path.with_extension("probe.duckdb");
    let works = connect(&probe).and_then(|mut conn| migrate::migrate(&mut conn).map(drop));
    let _ = backup::remove_with_wal(&probe);
    if let Err(probe_error) = &works {
        tracing::error!("a new database fails too ({probe_error:#}); not recovering");
    }
    works.is_ok()
}

/// Moves an unusable database aside and rebuilds it from the newest backup that restores.
fn recover(path: &Path, backups: &Path, quarantine: &Path) -> Result<(Connection, Opening)> {
    let quarantined = backup::quarantine(path, quarantine, &stamp())?;
    tracing::error!(
        "moved the unusable progress database to {}",
        quarantined.display()
    );
    for file in backup::newest_first(backups)? {
        let restored = backup::restore(&file, path).and_then(|()| {
            let mut conn = connect(path)?;
            migrate::migrate(&mut conn).context(SetupFailed)?;
            Ok(conn)
        });
        match restored {
            Ok(conn) => {
                tracing::error!("restored the progress database from {}", file.display());
                return Ok((
                    conn,
                    Opening::Recovered {
                        quarantined,
                        backup: Some(file),
                    },
                ));
            }
            Err(error) if error.downcast_ref::<SetupFailed>().is_some() => {
                return Err(error).with_context(|| {
                    format!("restored {} but could not migrate it", file.display())
                });
            }
            Err(error) => {
                tracing::error!("backup {} does not restore: {error:#}", file.display());
                backup::remove_with_wal(path)?;
            }
        }
    }
    tracing::error!(
        "no usable backup in {}; starting with an empty progress database",
        backups.display()
    );
    let mut conn = connect(path)?;
    migrate::migrate(&mut conn)?;
    Ok((
        conn,
        Opening::Recovered {
            quarantined,
            backup: None,
        },
    ))
}

impl Store {
    /// Opens (or creates) the progress database at `path` and migrates it, then attaches the
    /// test corpus at `corpus` read-only. A database that cannot be opened is quarantined and
    /// restored from `backups/` next to it (see [`Opening::Recovered`]). Backup or migration
    /// failures on an openable database stop startup and leave its files in place.
    pub fn open(path: &Path, corpus: &Path) -> Result<(Self, Opening)> {
        let dir = path.parent().unwrap_or_else(|| Path::new("."));
        std::fs::create_dir_all(dir)?;
        let backups = dir.join("backups");
        let (conn, opening) = match open_and_migrate(path, &backups) {
            Ok(opened) => opened,
            Err(error) if recoverable(&error, path) => {
                tracing::error!(
                    "the progress database {} is unusable: {error:#}",
                    path.display()
                );
                recover(path, &backups, &dir.join("quarantine"))?
            }
            Err(error) => return Err(error),
        };
        let corpus = corpus::attach(&conn, corpus).unwrap_or_else(|error| {
            tracing::error!("{error:#}; nothing can be judged");
            None
        });
        let store = Self {
            conn: Mutex::new(conn),
            corpus,
            backups,
        };
        Ok((store, opening))
    }

    fn with<T>(&self, f: impl FnOnce(&Connection) -> duckdb::Result<T>) -> Result<T> {
        Ok(f(&self.conn.lock())?)
    }

    /// Holds the connection, as a long query would.
    #[cfg(test)]
    pub fn hold(&self) -> parking_lot::MutexGuard<'_, Connection> {
        self.conn.lock()
    }

    /// Whether the database answers a trivial query, waiting at most `wait` for the connection.
    pub fn ping(&self, wait: Duration) -> bool {
        self.conn
            .try_lock_for(wait)
            .is_some_and(|c| c.execute_batch("SELECT 1").is_ok())
    }

    /// Imports the SQLite database servers used before DuckDB, if there is one.
    pub fn import_sqlite(&self, path: &Path) -> Result<Option<Imported>> {
        if !path.exists() {
            return Ok(None);
        }
        sqlite::import(&mut self.conn.lock(), path).map(Some)
    }

    /// Takes the day's backup unless there is one (see [`backup::daily`]).
    pub fn backup(&self, day: Date) -> Result<Option<Backup>> {
        backup::daily(&self.conn.lock(), &self.backups, day)
    }

    /// The whole attempt log, oldest first.
    pub fn attempts(&self) -> Result<Vec<Attempt>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT slug, epoch_ms(answered_at), grade::VARCHAR,
                    to_json(guessed_topics)::VARCHAR, topic_score, hints_used
                 FROM attempts ORDER BY answered_at, id",
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
            c.prepare_cached(
                "INSERT INTO attempts (slug, answered_at, grade, guessed_topics, topic_score,
                    hints_used)
                 VALUES (?, to_timestamp(? / 1000), ?, json(?)::VARCHAR[], ?, ?)",
            )?
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
            c.prepare_cached(
                "INSERT OR REPLACE INTO daily_scores
                    (scored_on, computed_at, readiness, coverage, accuracy)
                 VALUES (?::DATE, to_timestamp(? / 1000), ?, ?, ?)",
            )?
            .execute(params![s.day, at, s.readiness, s.coverage, s.accuracy])
            .map(drop)
        })
    }

    /// The last `limit` days with a score, oldest first.
    pub fn daily_scores(&self, limit: usize) -> Result<Vec<DailyScore>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT strftime(scored_on, '%Y-%m-%d'), readiness, coverage, accuracy
                 FROM (FROM daily_scores ORDER BY scored_on DESC LIMIT ?) ORDER BY scored_on",
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
            let mut stmt = c.prepare("SELECT slug, body FROM notes")?;
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
                    "INSERT INTO notes (slug, body, updated_at)
                     VALUES (?, ?, to_timestamp(? / 1000))
                     ON CONFLICT (slug) DO UPDATE
                         SET body = excluded.body, updated_at = excluded.updated_at",
                )?
                .execute(params![slug, text, at])
                .map(drop)
            }
        })
    }

    /// Saves the editor's code ('' for "back to the starter"), keeping any previous version.
    pub fn save_draft(&self, slug: &str, code: &str, at: i64) -> Result<()> {
        self.with(|c| {
            if code.is_empty() {
                // Back to the starter: a row with nothing left to keep goes.
                c.prepare_cached("DELETE FROM drafts WHERE slug = ? AND previous_code IS NULL")?
                    .execute([slug])?;
                c.prepare_cached(
                    "UPDATE drafts SET code = NULL, updated_at = to_timestamp(? / 1000)
                     WHERE slug = ?",
                )?
                .execute(params![at, slug])
                .map(drop)
            } else {
                c.prepare_cached(
                    "INSERT INTO drafts (slug, code, updated_at)
                     VALUES (?, ?, to_timestamp(? / 1000))
                     ON CONFLICT (slug) DO UPDATE
                         SET code = excluded.code, updated_at = excluded.updated_at",
                )?
                .execute(params![slug, code, at])
                .map(drop)
            }
        })
    }

    /// A problem's draft; empty when there is none.
    pub fn draft(&self, slug: &str) -> Result<Draft> {
        let row = self.with(|c| {
            c.prepare_cached("SELECT code, previous_code FROM drafts WHERE slug = ?")?
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
        if current.is_empty() {
            self.save_draft(slug, "", at)?;
        } else {
            self.with(|c| {
                c.prepare_cached(
                    "INSERT INTO drafts (slug, code, previous_code, updated_at)
                     VALUES (?, NULL, ?, to_timestamp(? / 1000))
                     ON CONFLICT (slug) DO UPDATE SET code = NULL,
                         previous_code = excluded.previous_code, updated_at = excluded.updated_at",
                )?
                .execute(params![slug, current, at])
                .map(drop)
            })?;
        }
        self.draft(slug)
    }

    /// Restore: the previous version comes back and `current` becomes the previous one, so
    /// Restore again undoes it. `None` when there is nothing to restore.
    pub fn restore_draft(&self, slug: &str, current: &str, at: i64) -> Result<Option<Draft>> {
        let restored = self.with(|c| {
            c.prepare_cached(
                "UPDATE drafts SET code = previous_code, previous_code = nullif(?, ''),
                    updated_at = to_timestamp(? / 1000)
                 WHERE slug = ? AND previous_code IS NOT NULL",
            )?
            .execute(params![current, at, slug])
        })?;
        if restored == 0 {
            return Ok(None);
        }
        self.draft(slug).map(Some)
    }

    /// A problem's tests in order; none without a corpus.
    pub fn tests(&self, slug: &str) -> Result<Vec<TestRow>> {
        match &self.corpus {
            Some(corpus) => corpus.tests(&self.conn.lock(), slug),
            None => Ok(Vec::new()),
        }
    }

    /// Stores a judged submission and returns its id. Only the problem's newest
    /// [`SUBMISSIONS_KEPT`] are kept, plus its latest accepted one (which marks it solved);
    /// older ones go in the same transaction.
    pub fn insert_submission(&self, s: &NewSubmission) -> Result<i64> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let id = tx
            .prepare_cached(
                "INSERT INTO submissions (slug, submitted_at, code, verdict, tests_passed,
                    tests_total, cpu_ms, detail)
                 VALUES (?, to_timestamp(? / 1000), ?, ?, ?, ?, ?, ?::JSON::VARIANT)
                 RETURNING id",
            )?
            .query_row(
                params![
                    s.slug, s.at, s.code, s.verdict, s.passed, s.total, s.cpu_ms, s.detail
                ],
                |r| r.get(0),
            )?;
        tx.prepare_cached(
            "DELETE FROM submissions WHERE slug = $1
                AND id NOT IN (SELECT id FROM submissions WHERE slug = $1 ORDER BY id DESC LIMIT $2)
                AND id IS DISTINCT FROM (SELECT max(id) FROM submissions
                                         WHERE slug = $1 AND verdict = 'accepted')",
        )?
        .execute(params![s.slug, SUBMISSIONS_KEPT])?;
        tx.commit()?;
        Ok(id)
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

    /// Every stored submission's problem, time and verdict, replayed in the order they were
    /// judged. Submissions pruned for space (see [`Self::insert_submission`]) are not in it.
    pub fn coding_log(&self) -> Result<CodingLog> {
        let rows: Vec<(String, i64, String)> = self.with(|c| {
            let mut stmt = c.prepare(
                "SELECT slug, epoch_ms(submitted_at), verdict::VARCHAR FROM submissions ORDER BY id",
            )?;
            let rows = stmt.query_map([], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)))?;
            rows.collect()
        })?;
        let mut log = CodingLog::default();
        for (slug, at, verdict) in rows {
            let verdict = verdict_named(&verdict).context("an unknown verdict in submissions")?;
            log.record(&slug, at, verdict);
        }
        Ok(log)
    }

    /// Flushes the write-ahead log into the database file.
    pub fn checkpoint(&self) -> Result<()> {
        self.with(|c| c.execute_batch("CHECKPOINT"))
    }
}

#[cfg(test)]
pub mod testing {
    use std::path::{Path, PathBuf};
    use std::sync::atomic::{AtomicUsize, Ordering};

    /// A fresh directory under the system's temporary one, removed on drop.
    pub struct TempDir(PathBuf);

    impl TempDir {
        pub fn new(name: &str) -> Self {
            static NEXT: AtomicUsize = AtomicUsize::new(0);
            let dir = std::env::temp_dir().join(format!(
                "openleet-{name}-{}-{}",
                std::process::id(),
                NEXT.fetch_add(1, Ordering::Relaxed)
            ));
            let _ = std::fs::remove_dir_all(&dir);
            std::fs::create_dir_all(&dir).expect("temp dir");
            Self(dir)
        }

        pub fn path(&self, name: &str) -> PathBuf {
            self.0.join(name)
        }

        pub fn root(&self) -> &Path {
            &self.0
        }
    }

    impl Drop for TempDir {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::testing::TempDir;
    use super::*;
    use openleet_proto::Expected;

    fn store() -> (Store, TempDir) {
        let dir = TempDir::new("db");
        let (store, opening) =
            Store::open(&dir.path("openleet.duckdb"), &dir.path("missing.duckdb")).unwrap();
        assert!(matches!(opening, Opening::Created));
        (store, dir)
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
        store
            .insert_attempt(&attempt("b", 1_793_316_907_567, Grade::Good))
            .unwrap();
        store
            .insert_attempt(&attempt("a", 1_793_316_907_566, Grade::Again))
            .unwrap();
        let all = store.attempts().unwrap();
        assert_eq!(
            all.iter()
                .map(|a| (a.slug.as_str(), a.at))
                .collect::<Vec<_>>(),
            [("a", 1_793_316_907_566), ("b", 1_793_316_907_567)]
        );
        assert_eq!(all[0].grade, Grade::Again);
        assert_eq!(all[0].guessed, ["Array", "Hash Table"]);
        store.delete_attempts(Some("a")).unwrap();
        assert_eq!(store.attempts().unwrap().len(), 1);
        store.delete_attempts(None).unwrap();
        assert_eq!(store.attempts().unwrap().len(), 0);
    }

    #[test]
    fn millisecond_times_round_trip_exactly() {
        let dir = TempDir::new("db-times");
        let conn = connect(&dir.path("t.duckdb")).unwrap();
        // 1970, 2023, the production data's 2026, and the last million milliseconds of 2199.
        for start in [
            0_i64,
            1_700_000_000_000,
            1_793_316_000_000,
            7_258_117_400_000,
        ] {
            let wrong: i64 = conn
                .query_row(
                    "SELECT count(*) FROM range(?, ? + 1000000) t(ms)
                     WHERE epoch_ms(to_timestamp(ms / 1000)) <> ms",
                    [start, start],
                    |r| r.get(0),
                )
                .unwrap();
            assert_eq!(wrong, 0, "from {start}");
        }
    }

    #[test]
    fn constraints_reject_impossible_rows() {
        let (store, _dir) = store();
        let skip_with_score = Attempt {
            score: Some(0.5),
            ..attempt("a", 1, Grade::Skip)
        };
        assert!(store.insert_attempt(&skip_with_score).is_err());
        assert!(store.insert_attempt(&attempt("", 1, Grade::Good)).is_err());
        let too_many_hints = Attempt {
            hints: 11,
            ..attempt("a", 1, Grade::Good)
        };
        assert!(store.insert_attempt(&too_many_hints).is_err());
        let more_passed_than_total = NewSubmission {
            slug: "a",
            at: 1,
            code: "x",
            verdict: "accepted",
            passed: 2,
            total: 1,
            cpu_ms: 0,
            detail: "null",
        };
        assert!(store.insert_submission(&more_passed_than_total).is_err());
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
        let rows: i64 = store
            .with(|c| c.query_row("SELECT count(*) FROM drafts", [], |r| r.get(0)))
            .unwrap();
        assert_eq!(rows, 0, "an empty draft with no previous version is no row");
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
        // Reset of an empty editor with nothing saved leaves no row.
        assert!(store.reset_draft("c", "", 7).unwrap().previous.is_none());
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
            at: 1_793_316_000_004,
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
        assert_eq!(list[0].at, 1_793_316_000_004);
        let one = store.submission(first).unwrap().unwrap();
        assert_eq!(one.code.as_deref(), Some("print(1)"));
        let detail: serde_json::Value = serde_json::from_str(one.detail.unwrap().get()).unwrap();
        assert_eq!(detail["failing"]["kind"], "hidden");
        let log = store.coding_log().unwrap();
        assert!(log.solved("a") && !log.problem("a").unwrap().first_try());
    }

    #[test]
    fn keeps_the_newest_submissions_and_the_latest_accepted_one() {
        let (store, _dir) = store();
        let submit = |slug, verdict| {
            store
                .insert_submission(&NewSubmission {
                    slug,
                    at: 1,
                    code: "x",
                    verdict,
                    passed: 0,
                    total: 1,
                    cpu_ms: 1,
                    detail: "null",
                })
                .unwrap()
        };
        let accepted = submit("a", "accepted");
        let other = submit("b", "wrong_answer");
        let mut last = 0;
        for _ in 0..SUBMISSIONS_KEPT + 5 {
            last = submit("a", "wrong_answer");
        }
        let kept = store.submissions("a", 1000).unwrap();
        assert_eq!(kept.len(), SUBMISSIONS_KEPT + 1);
        assert_eq!(kept[0].id, last);
        assert_eq!(kept[SUBMISSIONS_KEPT].id, accepted);
        // The first Accepted is kept, so the problem stays solved after a restart.
        assert!(store.coding_log().unwrap().solved("a"));
        assert_eq!(store.submissions("b", 10).unwrap()[0].id, other);
    }

    #[test]
    fn reads_tests_from_the_attached_corpus() {
        let dir = TempDir::new("db-corpus");
        let corpus = dir.path("tests.duckdb");
        Connection::open(&corpus)
            .unwrap()
            .execute_batch(
                "CREATE TABLE tests (slug VARCHAR, idx USMALLINT, kind VARCHAR, test VARCHAR,
                    expected VARCHAR, expected_sha256 VARCHAR);
                 INSERT INTO tests VALUES ('a', 0, 'example', '{\"input\":{}}', '[1, 2]', NULL);",
            )
            .unwrap();
        let (store, _) = Store::open(&dir.path("openleet.duckdb"), &corpus).unwrap();
        let tests = store.tests("a").unwrap();
        assert!(matches!(&tests[0].expected, Expected::Value(v) if v.get() == "[1, 2]"));
    }

    /// A SQLite database as servers left it before DuckDB, with every table.
    fn old_sqlite(path: &Path, with_hints: bool) {
        let old = rusqlite::Connection::open(path).unwrap();
        let hints = if with_hints {
            ", hints INTEGER NOT NULL DEFAULT 0"
        } else {
            ""
        };
        old.execute_batch(&format!(
            "CREATE TABLE attempts (id INTEGER PRIMARY KEY, slug TEXT NOT NULL, at INTEGER NOT NULL,
                grade TEXT NOT NULL, guessed TEXT NOT NULL DEFAULT '[]', score REAL{hints});
             CREATE TABLE daily_scores (day TEXT PRIMARY KEY, at INTEGER NOT NULL,
                readiness REAL NOT NULL, coverage REAL NOT NULL, accuracy REAL);
             CREATE TABLE notes (slug TEXT PRIMARY KEY, text TEXT NOT NULL, at INTEGER NOT NULL);
             INSERT INTO attempts (slug, at, grade, guessed, score)
                VALUES ('is-subsequence', 1793327257719, 'less', '[\"Array\",\"Two Pointers\"]', 0.4),
                       ('two-sum', 1793316907566, 'skip', '[]', NULL);
             INSERT INTO daily_scores VALUES
                ('2026-10-29', 1793343472296, 0.00076930108636657178, 0.0012610340479192938, 0.4),
                ('2026-10-30', 1793429873666, 0.5, 1.0, NULL);
             INSERT INTO notes VALUES ('two-sum', 'Use a hash map.', 1793314419541);"
        ))
        .unwrap();
    }

    #[test]
    fn imports_every_table_of_the_old_sqlite_database() {
        for with_hints in [true, false] {
            let (store, dir) = store();
            let path = dir.path("progress.db");
            old_sqlite(&path, with_hints);
            let imported = store.import_sqlite(&path).unwrap().unwrap();
            assert_eq!(
                imported,
                Imported {
                    attempts: 2,
                    notes: 1,
                    daily_scores: 2
                }
            );
            let attempts = store.attempts().unwrap();
            assert_eq!(
                attempts
                    .iter()
                    .map(|a| (a.slug.as_str(), a.at, a.score, a.hints))
                    .collect::<Vec<_>>(),
                [
                    ("two-sum", 1_793_316_907_566, None, 0),
                    ("is-subsequence", 1_793_327_257_719, Some(0.4), 0)
                ]
            );
            assert_eq!(attempts[1].guessed, ["Array", "Two Pointers"]);
            assert_eq!(store.notes().unwrap()["two-sum"], "Use a hash map.");
            let days = store.daily_scores(60).unwrap();
            assert_eq!(days.len(), 2);
            assert_eq!(days[0].day, "2026-10-29");
            assert_eq!(
                days[0].readiness.to_bits(),
                0.000_769_301_086_366_571_8_f64.to_bits()
            );
            assert_eq!(days[1].accuracy, None);
            let at: i64 = store
                .with(|c| {
                    c.query_row(
                        "SELECT epoch_ms(computed_at) FROM daily_scores ORDER BY scored_on LIMIT 1",
                        [],
                        |r| r.get(0),
                    )
                })
                .unwrap();
            assert_eq!(at, 1_793_343_472_296);
        }
    }

    #[test]
    fn imports_sqlite_only_into_a_new_database() {
        let dir = TempDir::new("db-sqlite-once");
        let path = dir.path("openleet.duckdb");
        let (_, first) = Store::open(&path, &dir.path("none")).unwrap();
        assert!(first.started_empty());
        let (_, second) = Store::open(&path, &dir.path("none")).unwrap();
        assert!(!second.started_empty());
    }

    #[test]
    fn backs_up_rotates_and_recovers_a_corrupt_database() {
        let dir = TempDir::new("db-recover");
        let path = dir.path("openleet.duckdb");
        {
            let (store, _) = Store::open(&path, &dir.path("none")).unwrap();
            store
                .insert_attempt(&attempt("a", 1_793_316_907_566, Grade::Good))
                .unwrap();
            store.save_note("a", "note", 2).unwrap();
            store.save_draft("a", "code", 3).unwrap();
            let id = store
                .insert_submission(&NewSubmission {
                    slug: "a",
                    at: 4,
                    code: "print(1)",
                    verdict: "accepted",
                    passed: 1,
                    total: 1,
                    cpu_ms: 5,
                    detail: r#"{"limitMs":2000}"#,
                })
                .unwrap();
            assert_eq!(id, 1);
            // Sixteen days of backups; only the newest fourteen stay.
            for day in 1..=16 {
                let day = Date::new(2026, 11, day).unwrap();
                assert!(store.backup(day).unwrap().is_some());
            }
            assert!(
                store
                    .backup(Date::new(2026, 11, 16).unwrap())
                    .unwrap()
                    .is_none()
            );
            let kept = backup::newest_first(&dir.path("backups")).unwrap();
            assert_eq!(kept.len(), backup::KEEP);
            assert!(
                kept[0].ends_with("2026-11-16.duckdb") && kept[13].ends_with("2026-11-03.duckdb")
            );
            store.checkpoint().unwrap();
        }
        // Corrupt the file: overwrite its headers.
        let mut bytes = std::fs::read(&path).unwrap();
        bytes[..16384].fill(0xAB);
        std::fs::write(&path, bytes).unwrap();

        let (store, opening) = Store::open(&path, &dir.path("none")).unwrap();
        let Opening::Recovered {
            quarantined,
            backup: Some(backup),
        } = opening
        else {
            panic!("expected a recovery from a backup, got {opening:?}");
        };
        assert!(backup.ends_with("2026-11-16.duckdb"));
        assert!(quarantined.join("openleet.duckdb").exists());
        let attempts = store.attempts().unwrap();
        assert_eq!(attempts[0].at, 1_793_316_907_566);
        assert_eq!(store.notes().unwrap()["a"], "note");
        assert_eq!(store.draft("a").unwrap().code.as_deref(), Some("code"));
        let one = store.submission(1).unwrap().unwrap();
        assert_eq!(one.detail.unwrap().get(), r#"{"limitMs":2000}"#);
        // Ids continue after the restored ones.
        let next = store
            .insert_submission(&NewSubmission {
                slug: "a",
                at: 5,
                code: "x",
                verdict: "wrong_answer",
                passed: 0,
                total: 1,
                cpu_ms: 1,
                detail: "null",
            })
            .unwrap();
        assert_eq!(next, 2);
        // The restored schema is the migrated one, comments included.
        let comment: Option<String> = store
            .with(|c| {
                c.query_row(
                    "SELECT comment FROM duckdb_tables() WHERE table_name = 'attempts'",
                    [],
                    |r| r.get(0),
                )
            })
            .unwrap();
        assert!(comment.is_some());
    }

    #[test]
    fn recovers_empty_without_a_backup() {
        let dir = TempDir::new("db-recover-empty");
        let path = dir.path("openleet.duckdb");
        std::fs::write(&path, b"not a database").unwrap();
        let (store, opening) = Store::open(&path, &dir.path("none")).unwrap();
        assert!(opening.started_empty());
        assert_eq!(store.attempts().unwrap().len(), 0);
        let Opening::Recovered { quarantined, .. } = opening else {
            panic!("expected a recovery");
        };
        assert_eq!(
            std::fs::read(quarantined.join("openleet.duckdb")).unwrap(),
            b"not a database"
        );
    }

    #[test]
    fn setup_failures_never_replace_an_openable_database() {
        for blocked_backup in [true, false] {
            let dir = TempDir::new("db-setup-failure");
            let path = dir.path("openleet.duckdb");
            Connection::open(&path)
                .unwrap()
                .execute_batch(
                    "CREATE TABLE notes (slug VARCHAR, text VARCHAR, at_ms BIGINT);
                     INSERT INTO notes VALUES ('a', 'keep this note', 123);
                     CREATE TABLE attempts (unexpected VARCHAR);",
                )
                .unwrap();
            if blocked_backup {
                std::fs::write(dir.path("backups"), "not a directory").unwrap();
            }
            let error = match Store::open(&path, &dir.path("none")) {
                Ok(_) => panic!("setup should fail"),
                Err(error) => error,
            };
            assert!(error.downcast_ref::<SetupFailed>().is_some(), "{error:#}");
            assert!(!dir.path("quarantine").exists());
            let conn = Connection::open(&path).unwrap();
            let note: String = conn
                .query_row("SELECT text FROM notes", [], |r| r.get(0))
                .unwrap();
            assert_eq!(note, "keep this note");
            assert_eq!(migrate::shape(&conn).unwrap(), Shape::Unversioned);
        }
    }

    #[test]
    fn recovery_does_not_skip_a_newer_schema_for_an_older_backup() {
        let dir = TempDir::new("db-recover-newer");
        let path = dir.path("openleet.duckdb");
        {
            let (store, _) = Store::open(&path, &dir.path("none")).unwrap();
            store.backup(Date::new(2026, 11, 9).unwrap()).unwrap();
            store.save_note("a", "latest data", 1).unwrap();
            store
                .with(|conn| {
                    conn.execute(
                        "INSERT INTO schema_migrations (version, name) VALUES (?, 'future')",
                        [migrate::latest() + 1],
                    )
                })
                .unwrap();
            store.backup(Date::new(2026, 11, 10).unwrap()).unwrap();
        }
        std::fs::write(&path, b"not a database").unwrap();
        let error = match Store::open(&path, &dir.path("none")) {
            Ok(_) => panic!("a newer backup must stop recovery, not roll back its data"),
            Err(error) => error,
        };
        assert!(
            error.downcast_ref::<migrate::NewerSchema>().is_some(),
            "{error:#}"
        );
        let conn = Connection::open(&path).unwrap();
        let note: String = conn
            .query_row("SELECT body FROM notes", [], |r| r.get(0))
            .unwrap();
        assert_eq!(note, "latest data");
    }

    #[test]
    fn backup_quotes_the_source_database_name() {
        let dir = TempDir::new("db-backup-quoted");
        let (store, _) = Store::open(&dir.path("my\"progress.duckdb"), &dir.path("none")).unwrap();
        store.save_note("a", "preserved", 1).unwrap();
        let backup = store
            .backup(Date::new(2026, 11, 10).unwrap())
            .unwrap()
            .unwrap();
        let conn = Connection::open(&backup.file).unwrap();
        let note: String = conn
            .query_row("SELECT body FROM notes", [], |r| r.get(0))
            .unwrap();
        assert_eq!(note, "preserved");
    }

    #[test]
    fn migrating_keeps_a_copy_of_the_old_file() {
        let dir = TempDir::new("db-snapshot");
        let path = dir.path("openleet.duckdb");
        Connection::open(&path)
            .unwrap()
            .execute_batch(
                "CREATE TYPE grade AS ENUM ('again', 'good', 'less', 'skip');
                 CREATE TABLE attempts (slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL,
                    grade grade NOT NULL, guessed VARCHAR[] NOT NULL, score DOUBLE,
                    hints UTINYINT NOT NULL);
                 INSERT INTO attempts VALUES ('two-sum', 1793316907566, 'good', [], 1.0, 0);",
            )
            .unwrap();
        let (store, opening) = Store::open(&path, &dir.path("none")).unwrap();
        assert!(matches!(opening, Opening::Existing(m) if m.from == Shape::Unversioned));
        assert_eq!(store.attempts().unwrap()[0].at, 1_793_316_907_566);
        let copies: Vec<_> = std::fs::read_dir(dir.path("backups"))
            .unwrap()
            .filter_map(Result::ok)
            .filter(|e| {
                e.file_name()
                    .to_string_lossy()
                    .starts_with("pre-migration-")
            })
            .collect();
        assert_eq!(copies.len(), 1);
        let copy = Connection::open(copies[0].path()).unwrap();
        let legacy: i64 = copy
            .query_row("SELECT count(*) FROM attempts WHERE at_ms > 0", [], |r| {
                r.get(0)
            })
            .unwrap();
        assert_eq!(legacy, 1, "the copy keeps the old shape");
    }
}
