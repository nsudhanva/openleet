//! Daily backups of the progress database, and recovery from them.
//!
//! DuckDB lets one process open a database file, so the server itself takes the backups:
//! `COPY FROM DATABASE` into a new DuckDB file, `STATE_DIR/backups/<UTC date>.duckdb`, written
//! under a temporary name and renamed into place, keeping the newest [`KEEP`]. A DuckDB file
//! (compressed with DuckDB's own column encodings) keeps everything `EXPORT DATABASE` would
//! lose or need an extension for: named enum types, constraints, comments and the sequences'
//! positions, so restoring one is opening it (and migrating it if this build is newer). The
//! server's DuckDB has no Parquet extension, and needs none for this.
//!
//! Before migrating an existing database, a copy is taken the same way
//! (`backups/pre-migration-<stamp>.duckdb`; never rotated), so even the unversioned shape
//! remains at hand.

use std::path::{Path, PathBuf};

use anyhow::{Context, Result};
use duckdb::Connection;
use jiff::civil::Date;

use super::sql_string;

/// Daily backups kept.
pub const KEEP: usize = 14;
/// The prefix of a backup still being written.
const PARTIAL: &str = ".partial-";
const EXTENSION: &str = "duckdb";

/// A finished backup.
#[derive(Debug)]
pub struct Backup {
    pub file: PathBuf,
    pub bytes: u64,
}

/// Copies the database into `backups/<day>.duckdb`, unless that backup exists, and removes
/// the oldest backups beyond [`KEEP`].
pub fn daily(conn: &Connection, backups: &Path, day: Date) -> Result<Option<Backup>> {
    let file = backups.join(format!("{day}.{EXTENSION}"));
    if file.exists() {
        return Ok(None);
    }
    copy(conn, &file)?;
    for old in rotate(backups, KEEP)? {
        tracing::info!("backup: removed {}", old.display());
    }
    let bytes = std::fs::metadata(&file)?.len();
    Ok(Some(Backup { file, bytes }))
}

/// Copies the database into `backups/pre-migration-<stamp>.duckdb`.
pub fn before_migrating(conn: &Connection, backups: &Path, stamp: &str) -> Result<PathBuf> {
    let file = backups.join(format!("pre-migration-{stamp}.{EXTENSION}"));
    copy(conn, &file)?;
    Ok(file)
}

/// Writes a complete copy of the connection's database to `file` (which must not exist):
/// first under a temporary name, then renamed, so `file` is never half written.
fn copy(conn: &Connection, file: &Path) -> Result<()> {
    let dir = file.parent().context("backup directory")?;
    std::fs::create_dir_all(dir)?;
    let name = file
        .file_name()
        .context("backup file name")?
        .to_string_lossy();
    let partial = dir.join(format!("{PARTIAL}{name}"));
    remove_with_wal(&partial)?;
    let source: String = conn.query_row("SELECT current_database()", [], |r| r.get(0))?;
    conn.execute_batch(&format!("ATTACH {} AS backup_target", sql_string(&partial)))?;
    let copied = conn.execute_batch(&format!(
        "COPY FROM DATABASE \"{}\" TO backup_target",
        source.replace('"', "\"\"")
    ));
    // Even a failed copy must release the alias and file before the next backup attempt.
    let detached = conn.execute_batch("DETACH backup_target");
    copied.with_context(|| format!("copying the database to {}", partial.display()))?;
    detached?;
    std::fs::rename(&partial, file)?;
    Ok(())
}

/// Daily backups in `backups`, newest first.
pub fn newest_first(backups: &Path) -> Result<Vec<PathBuf>> {
    let mut dated: Vec<(Date, PathBuf)> = match std::fs::read_dir(backups) {
        Ok(entries) => entries
            .filter_map(Result::ok)
            .filter_map(|e| {
                let path = e.path();
                if path.extension()? != EXTENSION {
                    return None;
                }
                let day: Date = path.file_stem()?.to_str()?.parse().ok()?;
                Some((day, path))
            })
            .collect(),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Vec::new(),
        Err(e) => return Err(e.into()),
    };
    dated.sort_by_key(|(day, _)| std::cmp::Reverse(*day));
    Ok(dated.into_iter().map(|(_, path)| path).collect())
}

/// Removes all but the newest `keep` daily backups and any interrupted copy; returns what
/// went.
pub fn rotate(backups: &Path, keep: usize) -> Result<Vec<PathBuf>> {
    let mut removed = newest_first(backups)?;
    removed.drain(..keep.min(removed.len()));
    for entry in std::fs::read_dir(backups)?.filter_map(Result::ok) {
        if entry.file_name().to_string_lossy().starts_with(PARTIAL) {
            removed.push(entry.path());
        }
    }
    for file in &removed {
        remove_with_wal(file)?;
    }
    Ok(removed)
}

/// Puts a copy of `backup` at `database` (which must not exist).
pub fn restore(backup: &Path, database: &Path) -> Result<()> {
    let partial = database.with_extension("restoring");
    std::fs::copy(backup, &partial).with_context(|| format!("copying {}", backup.display()))?;
    std::fs::rename(&partial, database)?;
    Ok(())
}

/// Moves the database file and its write-ahead log into `quarantine/<stamp>/`.
pub fn quarantine(database: &Path, quarantine: &Path, stamp: &str) -> Result<PathBuf> {
    let dir = quarantine.join(stamp);
    std::fs::create_dir_all(&dir)?;
    for file in [database.to_owned(), wal_of(database)] {
        if file.exists() {
            let name = file.file_name().context("database file name")?;
            std::fs::rename(&file, dir.join(name))
                .with_context(|| format!("quarantining {}", file.display()))?;
        }
    }
    Ok(dir)
}

/// The write-ahead log DuckDB keeps next to `database`.
pub fn wal_of(database: &Path) -> PathBuf {
    let mut name = database.as_os_str().to_owned();
    name.push(".wal");
    name.into()
}

/// Removes a database file and its write-ahead log, if there.
pub fn remove_with_wal(database: &Path) -> Result<()> {
    for file in [database.to_owned(), wal_of(database)] {
        match std::fs::remove_file(&file) {
            Err(e) if e.kind() != std::io::ErrorKind::NotFound => return Err(e.into()),
            _ => {}
        }
    }
    Ok(())
}
