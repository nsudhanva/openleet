//! The one-time import of the SQLite database (`progress.db`) servers used before DuckDB.
//!
//! Its shape varied by age: `attempts(id, slug, at, grade, guessed JSON text, score, hints)`
//! (`hints` came later), then `notes(slug, text, at)` and `daily_scores(day 'YYYY-MM-DD', at,
//! readiness, coverage, accuracy)`. Times are Unix milliseconds throughout.

use std::path::Path;

use anyhow::{Context, Result};
use duckdb::{Connection, params};
use rusqlite::OpenFlags;

/// Rows imported per table.
#[derive(Debug, Default, PartialEq, Eq)]
pub struct Imported {
    pub attempts: usize,
    pub notes: usize,
    pub daily_scores: usize,
}

struct Rows {
    attempts: Vec<(String, i64, String, String, Option<f64>, i64)>,
    notes: Vec<(String, String, i64)>,
    daily_scores: Vec<(String, i64, f64, f64, Option<f64>)>,
}

/// Copies every attempt, note and daily score of the SQLite database at `path` into `conn`,
/// in one transaction.
pub fn import(conn: &mut Connection, path: &Path) -> Result<Imported> {
    let rows = read(path).with_context(|| format!("reading {}", path.display()))?;
    let tx = conn.transaction()?;
    {
        // Attempt ids follow the old log's order (time, then its own id).
        let mut insert = tx.prepare(
            "INSERT INTO attempts (slug, answered_at, grade, guessed_topics, topic_score, hints_used)
             VALUES (?, to_timestamp(? / 1000), ?, json(?)::VARCHAR[], ?, ?)",
        )?;
        for (slug, at, grade, guessed, score, hints) in &rows.attempts {
            insert.execute(params![slug, at, grade, guessed, score, hints])?;
        }
        let mut insert = tx.prepare(
            "INSERT OR REPLACE INTO notes (slug, body, updated_at)
             VALUES (?, ?, to_timestamp(? / 1000))",
        )?;
        // An empty note meant none.
        for (slug, text, at) in rows.notes.iter().filter(|(_, text, _)| !text.is_empty()) {
            insert.execute(params![slug, text, at])?;
        }
        let mut insert = tx.prepare(
            "INSERT OR REPLACE INTO daily_scores (scored_on, computed_at, readiness, coverage, accuracy)
             VALUES (?::DATE, to_timestamp(? / 1000), ?, ?, ?)",
        )?;
        for (day, at, readiness, coverage, accuracy) in &rows.daily_scores {
            insert.execute(params![day, at, readiness, coverage, accuracy])?;
        }
    }
    tx.commit()?;
    Ok(Imported {
        attempts: rows.attempts.len(),
        notes: rows
            .notes
            .iter()
            .filter(|(_, text, _)| !text.is_empty())
            .count(),
        daily_scores: rows.daily_scores.len(),
    })
}

fn read(path: &Path) -> Result<Rows> {
    let old = rusqlite::Connection::open_with_flags(path, OpenFlags::SQLITE_OPEN_READ_ONLY)?;
    let has = |table: &str, column: &str| -> rusqlite::Result<bool> {
        old.query_row(
            "SELECT count(*) > 0 FROM pragma_table_info(?1) WHERE name = ?2",
            [table, column],
            |r| r.get(0),
        )
    };
    let hints = if has("attempts", "hints")? {
        "hints"
    } else {
        "0"
    };
    let attempts = old
        .prepare(&format!(
            "SELECT slug, at, grade, guessed, score, {hints} FROM attempts ORDER BY at, id"
        ))?
        .query_map([], |r| {
            Ok((
                r.get(0)?,
                r.get(1)?,
                r.get(2)?,
                r.get(3)?,
                r.get(4)?,
                r.get(5)?,
            ))
        })?
        .collect::<rusqlite::Result<_>>()?;
    let notes = if has("notes", "slug")? {
        old.prepare("SELECT slug, text, at FROM notes")?
            .query_map([], |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)))?
            .collect::<rusqlite::Result<_>>()?
    } else {
        Vec::new()
    };
    let daily_scores = if has("daily_scores", "day")? {
        old.prepare("SELECT day, at, readiness, coverage, accuracy FROM daily_scores ORDER BY day")?
            .query_map([], |r| {
                Ok((r.get(0)?, r.get(1)?, r.get(2)?, r.get(3)?, r.get(4)?))
            })?
            .collect::<rusqlite::Result<_>>()?
    } else {
        Vec::new()
    };
    Ok(Rows {
        attempts,
        notes,
        daily_scores,
    })
}
