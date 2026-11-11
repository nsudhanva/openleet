//! Versioned schema migrations for the progress database.
//!
//! Migrations are SQL files embedded in the binary, applied in version order, each in its own
//! transaction together with its row in `schema_migrations`, so a database is always at exactly
//! one known version and a failed migration leaves it at the previous one. Applied migrations
//! are never edited: a schema change is a new file appended to [`MIGRATIONS`].
//!
//! A database from before versioning (tables but no `schema_migrations`) is adopted in place:
//! its rows are set aside, migration 1 creates the clean schema and the rows are moved in, all
//! in one transaction (see `migrations/legacy_*.sql`).

use anyhow::{Context, Result, bail};
use duckdb::Connection;

/// One schema change.
pub struct Migration {
    pub version: u32,
    pub name: &'static str,
    sql: &'static str,
}

/// Every migration, in version order (versions are 1, 2, 3, ... with no gaps).
pub const MIGRATIONS: &[Migration] = &[
    Migration {
        version: 1,
        name: "progress",
        sql: include_str!("migrations/0001_progress.sql"),
    },
    Migration {
        version: 2,
        name: "plans",
        sql: include_str!("migrations/0002_plans.sql"),
    },
    Migration {
        version: 3,
        name: "shaky_plans",
        sql: include_str!("migrations/0003_shaky_plans.sql"),
    },
    Migration {
        version: 4,
        name: "metric_comments",
        sql: include_str!("migrations/0004_metric_comments.sql"),
    },
];

/// The version this build migrates databases to.
pub fn latest() -> u32 {
    MIGRATIONS.last().map_or(0, |m| m.version)
}

const LEDGER: &str = "
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY CHECK (version > 0),
    name VARCHAR NOT NULL CHECK (name <> ''),
    applied_at TIMESTAMPTZ NOT NULL DEFAULT current_timestamp
);
COMMENT ON TABLE schema_migrations IS 'Schema migrations applied to this database, one row each (server/src/db/migrate.rs).';
COMMENT ON COLUMN schema_migrations.version IS 'The migration''s version; the database is at the largest one.';
COMMENT ON COLUMN schema_migrations.name IS 'The migration''s name.';
COMMENT ON COLUMN schema_migrations.applied_at IS 'When the migration was applied.';
";
const LEGACY_STAGE: &str = include_str!("migrations/legacy_stage.sql");
const LEGACY_ADOPT: &str = include_str!("migrations/legacy_adopt.sql");
/// Moves the id sequences past the ids in their tables (after inserts with explicit ids).
const SYNC_SEQUENCES: &str = include_str!("migrations/sync_sequences.sql");

/// The tables an unversioned database may hold.
const LEGACY_TABLES: [&str; 5] = ["attempts", "daily_scores", "notes", "drafts", "submissions"];

/// What a database held before migrating.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Shape {
    /// No tables: a new database.
    Empty,
    /// Tables from before versioning.
    Unversioned,
    /// At this version.
    Version(u32),
}

/// The database's schema is newer than this build knows (a rollback across a migration).
/// Never treated as corruption: the database is fine, the binary is too old for it.
#[derive(Debug, thiserror::Error)]
#[error("the database is at schema version {found}, newer than this build's {known}")]
pub struct NewerSchema {
    pub found: u32,
    pub known: u32,
}

/// What [`migrate`] did.
#[derive(Debug, PartialEq, Eq)]
pub struct Migrated {
    pub from: Shape,
    pub to: u32,
}

impl Migrated {
    /// Whether any migration ran.
    pub fn changed(&self) -> bool {
        self.from != Shape::Version(self.to)
    }
}

/// The database's shape.
pub fn shape(conn: &Connection) -> Result<Shape> {
    let tables: Vec<String> = {
        let mut stmt = conn.prepare(
            "SELECT table_name FROM duckdb_tables()
             WHERE database_name = current_database() AND schema_name = 'main' AND NOT temporary",
        )?;
        stmt.query_map([], |r| r.get(0))?
            .collect::<duckdb::Result<_>>()?
    };
    if tables.iter().any(|t| t == "schema_migrations") {
        let version: Option<u32> =
            conn.query_row("SELECT max(version) FROM schema_migrations", [], |r| {
                r.get(0)
            })?;
        return Ok(Shape::Version(version.unwrap_or(0)));
    }
    if tables.is_empty() {
        return Ok(Shape::Empty);
    }
    if let Some(odd) = tables.iter().find(|t| !LEGACY_TABLES.contains(&t.as_str())) {
        bail!("unversioned database with an unknown table {odd}; refusing to migrate it");
    }
    Ok(Shape::Unversioned)
}

/// Applies every pending migration.
///
/// # Errors
/// [`NewerSchema`] when the database is ahead of this build; otherwise the failing
/// migration's error (that migration rolled back, earlier ones stay applied).
pub fn migrate(conn: &mut Connection) -> Result<Migrated> {
    migrate_to(conn, latest())
}

/// Applies the pending migrations up to and including `target`.
pub fn migrate_to(conn: &mut Connection, target: u32) -> Result<Migrated> {
    let from = shape(conn)?;
    let mut at = match from {
        Shape::Version(v) if v > latest() => {
            return Err(NewerSchema {
                found: v,
                known: latest(),
            }
            .into());
        }
        Shape::Version(v) => v,
        Shape::Empty => 0,
        Shape::Unversioned => {
            let first = &MIGRATIONS[0];
            apply(conn, first, Some((LEGACY_STAGE, LEGACY_ADOPT)))
                .context("adopting the unversioned database")?;
            first.version
        }
    };
    for migration in MIGRATIONS {
        if migration.version > at && migration.version <= target {
            apply(conn, migration, None)?;
            at = migration.version;
        }
    }
    Ok(Migrated { from, to: at })
}

/// Runs one migration and records it, in one transaction; `legacy` wraps it with the steps
/// that adopt an unversioned database.
fn apply(conn: &mut Connection, migration: &Migration, legacy: Option<(&str, &str)>) -> Result<()> {
    let tx = conn.transaction()?;
    tx.execute_batch(LEDGER)?;
    if let Some((stage, _)) = legacy {
        tx.execute_batch(stage)?;
    }
    tx.execute_batch(migration.sql)
        .with_context(|| format!("migration {} ({})", migration.version, migration.name))?;
    if let Some((_, adopt)) = legacy {
        tx.execute_batch(adopt)?;
        tx.execute_batch(SYNC_SEQUENCES)?;
    }
    tx.execute(
        "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
        duckdb::params![migration.version, migration.name],
    )?;
    tx.commit()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    #[test]
    fn versions_are_contiguous_from_one() {
        for (i, m) in MIGRATIONS.iter().enumerate() {
            assert_eq!(m.version as usize, i + 1, "{}", m.name);
        }
    }

    #[test]
    fn creates_a_fresh_database_and_reruns_as_a_no_op() {
        let dir = TempDir::new("migrate-fresh");
        let mut conn = Connection::open(dir.path("p.duckdb")).unwrap();
        let first = migrate(&mut conn).unwrap();
        assert_eq!(
            first,
            Migrated {
                from: Shape::Empty,
                to: latest()
            }
        );
        let again = migrate(&mut conn).unwrap();
        assert!(!again.changed());
        let rows: i64 = conn
            .query_row("SELECT count(*) FROM schema_migrations", [], |r| r.get(0))
            .unwrap();
        assert_eq!(rows, i64::from(latest()));
        // Reopening sees the same version.
        drop(conn);
        let mut conn = Connection::open(dir.path("p.duckdb")).unwrap();
        assert!(!migrate(&mut conn).unwrap().changed());
    }

    #[test]
    fn every_table_and_column_has_a_comment() {
        let dir = TempDir::new("migrate-comments");
        let mut conn = Connection::open(dir.path("p.duckdb")).unwrap();
        migrate(&mut conn).unwrap();
        let missing: Vec<String> = conn
            .prepare(
                "SELECT table_name FROM duckdb_tables() WHERE comment IS NULL
                 UNION ALL
                 SELECT table_name || '.' || column_name FROM duckdb_columns()
                 WHERE comment IS NULL AND NOT internal",
            )
            .unwrap()
            .query_map([], |r| r.get(0))
            .unwrap()
            .collect::<duckdb::Result<_>>()
            .unwrap();
        assert!(missing.is_empty(), "uncommented: {missing:?}");
    }

    #[test]
    fn migrates_a_version_1_database_to_plans_keeping_its_rows() {
        let dir = TempDir::new("migrate-v1");
        let path = dir.path("p.duckdb");
        {
            let mut conn = Connection::open(&path).unwrap();
            assert_eq!(migrate_to(&mut conn, 1).unwrap().to, 1);
            conn.execute_batch(
                "INSERT INTO attempts (slug, answered_at, grade, guessed_topics, topic_score,
                    hints_used) VALUES ('two-sum', to_timestamp(1793316907.566), 'good',
                    ['Array'], 1.0, 0);
                 INSERT INTO notes VALUES ('two-sum', 'Use a hash map.', to_timestamp(1));",
            )
            .unwrap();
            assert_eq!(shape(&conn).unwrap(), Shape::Version(1));
        }
        let mut conn = Connection::open(&path).unwrap();
        let migrated = migrate(&mut conn).unwrap();
        assert_eq!(
            migrated,
            Migrated {
                from: Shape::Version(1),
                to: latest()
            }
        );
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}', slug, epoch_ms(answered_at)) FROM attempts"
            ),
            ["two-sum|1793316907566"]
        );
        assert_eq!(
            strings(&conn, "SELECT body FROM notes"),
            ["Use a hash map."]
        );
        assert_eq!(
            strings(&conn, "SELECT name FROM schema_migrations ORDER BY version"),
            ["progress", "plans", "shaky_plans", "metric_comments"]
        );
        // Migration 4 changes only comments: the daily scores stay, described as kept data.
        let comment = strings(
            &conn,
            "SELECT comment FROM duckdb_tables() WHERE table_name = 'daily_scores'",
        );
        assert!(
            comment[0].contains("Neither written nor read"),
            "{comment:?}"
        );
        // The new table takes plans, with NULL filters, and rejects impossible ones.
        let id: i64 = conn
            .query_row(
                "INSERT INTO plans (company, period, status, sort_order, created_at, used_at)
                 VALUES ('google', '6m', 'unsolved', 'rank', now(), now()) RETURNING id",
                [],
                |r| r.get(0),
            )
            .unwrap();
        assert_eq!(id, 1);
        let insert = |columns: &str, values: &str| {
            conn.execute_batch(&format!(
                "INSERT INTO plans (company, period, status, sort_order{columns}, created_at, used_at)
                 VALUES ({values}, now(), now())"
            ))
        };
        insert(
            ", topic, difficulty, name",
            "'any', 'lc1000', 'all', 'random', 'Trie', 'Hard', 'Tries'",
        )
        .unwrap();
        for (columns, values) in [
            ("", "'google', '1y', 'all', 'rank'"),
            ("", "'google', '6m', 'solved', 'rank'"),
            ("", "'google', '6m', 'all', 'best'"),
            ("", "'', '6m', 'all', 'rank'"),
            (", topic", "'google', '6m', 'all', 'rank', ''"),
            (
                ", difficulty",
                "'google', '6m', 'all', 'rank', 'Impossible'",
            ),
            (", name", "'google', '6m', 'all', 'rank', ''"),
        ] {
            assert!(insert(columns, values).is_err(), "{columns} {values}");
        }
        let too_long = format!("'google', '6m', 'all', 'rank', '{}'", "x".repeat(61));
        assert!(insert(", name", &too_long).is_err());
    }

    #[test]
    fn migrates_version_2_plans_to_take_the_shaky_status() {
        let dir = TempDir::new("migrate-v2");
        let path = dir.path("p.duckdb");
        {
            let mut conn = Connection::open(&path).unwrap();
            migrate_to(&mut conn, 2).unwrap();
            conn.execute_batch(
                "INSERT INTO plans (company, period, topic, status, sort_order, name, pinned,
                    created_at, used_at)
                 VALUES ('google', '6m', 'Graph', 'untried', 'rank', 'Graphs', true,
                    to_timestamp(1), to_timestamp(2))",
            )
            .unwrap();
            assert!(
                conn.execute_batch(
                    "INSERT INTO plans (company, period, status, sort_order, created_at, used_at)
                     VALUES ('google', '6m', 'shaky', 'rank', now(), now())"
                )
                .is_err()
            );
        }
        let mut conn = Connection::open(&path).unwrap();
        assert_eq!(migrate(&mut conn).unwrap().from, Shape::Version(2));
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}|{}|{}', id, status, topic, name, pinned) FROM plans"
            ),
            ["1|untried|Graph|Graphs|true"]
        );
        let id: i64 = conn
            .query_row(
                "INSERT INTO plans (company, period, status, sort_order, created_at, used_at)
                 VALUES ('google', '6m', 'shaky', 'rank', now(), now()) RETURNING id",
                [],
                |r| r.get(0),
            )
            .unwrap();
        assert_eq!(id, 2, "the id sequence goes on");
        assert!(
            conn.execute_batch(
                "INSERT INTO plans (company, period, status, sort_order, created_at, used_at)
                 VALUES ('google', '6m', 'solved', 'rank', now(), now())"
            )
            .is_err()
        );
    }

    #[test]
    fn refuses_a_newer_schema() {
        let dir = TempDir::new("migrate-newer");
        let mut conn = Connection::open(dir.path("p.duckdb")).unwrap();
        migrate(&mut conn).unwrap();
        conn.execute(
            "INSERT INTO schema_migrations (version, name) VALUES (?, 'future')",
            [latest() + 1],
        )
        .unwrap();
        let error = migrate(&mut conn).unwrap_err();
        assert!(error.downcast_ref::<NewerSchema>().is_some(), "{error:#}");
    }

    #[test]
    fn refuses_an_unknown_unversioned_database() {
        let dir = TempDir::new("migrate-unknown");
        let mut conn = Connection::open(dir.path("p.duckdb")).unwrap();
        conn.execute_batch("CREATE TABLE something_else (x INTEGER)")
            .unwrap();
        assert!(migrate(&mut conn).is_err());
    }

    /// The shape servers wrote before versioning, with one row of every kind (two attempts
    /// in the same millisecond, an empty note and an empty draft the old code meant as none).
    const LEGACY: &str = r#"
        CREATE TYPE grade AS ENUM ('again', 'good', 'less', 'skip');
        CREATE TYPE verdict AS ENUM ('accepted', 'wrong_answer', 'time_limit_exceeded',
            'memory_limit_exceeded', 'runtime_error', 'compile_error', 'output_limit_exceeded',
            'internal_error');
        CREATE SEQUENCE submission_id START 1;
        CREATE TABLE attempts (slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL,
            grade grade NOT NULL, guessed VARCHAR[] NOT NULL, score DOUBLE,
            hints UTINYINT NOT NULL);
        CREATE TABLE daily_scores (day DATE PRIMARY KEY, at_ms BIGINT NOT NULL,
            readiness DOUBLE NOT NULL, coverage DOUBLE NOT NULL, accuracy DOUBLE);
        CREATE TABLE notes (slug VARCHAR PRIMARY KEY, text VARCHAR NOT NULL,
            at_ms BIGINT NOT NULL);
        CREATE TABLE drafts (slug VARCHAR PRIMARY KEY, code VARCHAR NOT NULL,
            at_ms BIGINT NOT NULL, previous VARCHAR);
        CREATE TABLE submissions (id BIGINT PRIMARY KEY DEFAULT nextval('submission_id'),
            slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL, code VARCHAR NOT NULL,
            verdict verdict NOT NULL, passed USMALLINT NOT NULL, total USMALLINT NOT NULL,
            cpu_ms UINTEGER NOT NULL, detail VARIANT);
        INSERT INTO attempts VALUES
            ('is-subsequence', 1793327257719, 'less', ['Array', 'Two Pointers'], 0.4, 2),
            ('two-sum', 1793316907566, 'skip', [], NULL, 0),
            ('add-two-numbers', 1793316907566, 'good', ['Linked List'], 1.0, 10);
        INSERT INTO daily_scores VALUES
            ('2026-10-29', 1793343472296, 0.00076930108636657178, 0.0012610340479192938, 0.4),
            ('2026-10-30', 1793429873666, 0.5, 1.0, NULL);
        INSERT INTO notes VALUES ('two-sum', 'Use a hash map.', 1793314419541),
            ('palindrome-number', '', 1793314419542);
        INSERT INTO drafts VALUES ('two-sum', 'class Solution: ...', 1793316000001, NULL),
            ('is-subsequence', '', 1793316000002, 'old code'),
            ('add-two-numbers', '', 1793316000003, NULL);
        INSERT INTO submissions (slug, at_ms, code, verdict, passed, total, cpu_ms, detail)
            VALUES ('two-sum', 1793316000004, 'print(1)', 'wrong_answer', 3, 9, 40,
                '{"failing":{"input":"x = 1","kind":"hidden"},"limitMs":2000}'::JSON::VARIANT),
            ('two-sum', 1793316000005, 'print(2)', 'accepted', 9, 9, 41, NULL);
        DELETE FROM submissions WHERE id = 1;
        INSERT INTO submissions (slug, at_ms, code, verdict, passed, total, cpu_ms)
            VALUES ('two-sum', 1793316000006, 'print(3)', 'compile_error', 0, 9, 0);
    "#;

    fn strings(conn: &Connection, sql: &str) -> Vec<String> {
        conn.prepare(sql)
            .unwrap()
            .query_map([], |r| r.get(0))
            .unwrap()
            .collect::<duckdb::Result<_>>()
            .unwrap()
    }

    #[test]
    fn adopts_an_unversioned_database_without_losing_data() {
        let dir = TempDir::new("migrate-legacy");
        let path = dir.path("p.duckdb");
        {
            let conn = Connection::open(&path).unwrap();
            conn.execute_batch(LEGACY).unwrap();
        }
        let mut conn = Connection::open(&path).unwrap();
        let migrated = migrate(&mut conn).unwrap();
        assert_eq!(migrated.from, Shape::Unversioned);
        assert!(!migrate(&mut conn).unwrap().changed());

        // Attempts: ordered by time then insertion, times exact to the millisecond.
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}|{}|{}|{}|{}', id, slug, epoch_ms(answered_at), grade,
                    guessed_topics, ifnull(topic_score::VARCHAR, 'NULL'), hints_used) FROM attempts ORDER BY id"
            ),
            [
                "1|two-sum|1793316907566|skip|[]|NULL|0",
                "2|add-two-numbers|1793316907566|good|[Linked List]|1.0|10",
                "3|is-subsequence|1793327257719|less|[Array, Two Pointers]|0.4|2",
            ]
        );
        // Doubles survive bit for bit.
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}|{}|{}', scored_on, epoch_ms(computed_at),
                    readiness = 0.00076930108636657178, coverage, ifnull(accuracy::VARCHAR, 'NULL'))
                 FROM daily_scores ORDER BY scored_on"
            ),
            [
                "2026-10-29|1793343472296|true|0.0012610340479192938|0.4",
                "2026-10-30|1793429873666|false|1.0|NULL",
            ]
        );
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}', slug, body, epoch_ms(updated_at)) FROM notes"
            ),
            ["two-sum|Use a hash map.|1793314419541"]
        );
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}|{}', slug, ifnull(code, 'NULL'),
                    ifnull(previous_code, 'NULL'), epoch_ms(updated_at))
                 FROM drafts ORDER BY slug"
            ),
            [
                "is-subsequence|NULL|old code|1793316000002",
                "two-sum|class Solution: ...|NULL|1793316000001",
            ]
        );
        // Submission ids are kept (gaps included) and new ones continue after them.
        assert_eq!(
            strings(
                &conn,
                "SELECT format('{}|{}|{}|{}|{}|{}|{}|{}', id, epoch_ms(submitted_at), code,
                    verdict, tests_passed, tests_total, cpu_ms, ifnull(detail::JSON::VARCHAR, 'NULL'))
                 FROM submissions ORDER BY id"
            ),
            [
                "2|1793316000005|print(2)|accepted|9|9|41|NULL",
                "3|1793316000006|print(3)|compile_error|0|9|0|NULL",
            ]
        );
        let next: (i64, i64) = conn
            .query_row(
                "SELECT nextval('attempt_id_seq'), nextval('submission_id_seq')",
                [],
                |r| Ok((r.get(0)?, r.get(1)?)),
            )
            .unwrap();
        assert_eq!(next, (4, 4));
        // Nothing of the old schema is left.
        assert_eq!(
            strings(
                &conn,
                "SELECT sequence_name FROM duckdb_sequences() WHERE sequence_name = 'submission_id'
                 UNION ALL SELECT table_name FROM duckdb_tables() WHERE temporary"
            ),
            Vec::<String>::new()
        );
    }

    #[test]
    fn keeps_variant_details_when_adopting() {
        let dir = TempDir::new("migrate-variant");
        let path = dir.path("p.duckdb");
        {
            let conn = Connection::open(&path).unwrap();
            conn.execute_batch(LEGACY).unwrap();
            conn.execute_batch(
                "INSERT INTO submissions (slug, at_ms, code, verdict, passed, total, cpu_ms, detail)
                 VALUES ('a', 1, 'x', 'wrong_answer', 1, 2, 3,
                    '{\"failing\":{\"kind\":\"hidden\"},\"limitMs\":2000}'::JSON::VARIANT)",
            )
            .unwrap();
        }
        let mut conn = Connection::open(&path).unwrap();
        migrate(&mut conn).unwrap();
        let detail: String = conn
            .query_row(
                "SELECT detail::JSON::VARCHAR FROM submissions WHERE slug = 'a'",
                [],
                |r| r.get(0),
            )
            .unwrap();
        let value: serde_json::Value = serde_json::from_str(&detail).unwrap();
        assert_eq!(value["failing"]["kind"], "hidden");
        assert_eq!(value["limitMs"], 2000);
    }

    #[test]
    fn adopts_an_older_unversioned_database_without_drafts_or_submissions() {
        let dir = TempDir::new("migrate-older");
        let path = dir.path("p.duckdb");
        {
            let conn = Connection::open(&path).unwrap();
            conn.execute_batch(
                "CREATE TYPE grade AS ENUM ('again', 'good', 'less', 'skip');
                 CREATE TABLE attempts (slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL,
                    grade grade NOT NULL, guessed VARCHAR[] NOT NULL, score DOUBLE,
                    hints UTINYINT NOT NULL);
                 INSERT INTO attempts VALUES ('two-sum', 5, 'again', ['Array'], 0.5, 0);",
            )
            .unwrap();
        }
        let mut conn = Connection::open(&path).unwrap();
        assert_eq!(migrate(&mut conn).unwrap().from, Shape::Unversioned);
        assert_eq!(
            strings(&conn, "SELECT slug FROM attempts"),
            ["two-sum".to_owned()]
        );
    }

    #[test]
    fn a_failed_adoption_leaves_the_database_untouched() {
        let dir = TempDir::new("migrate-rollback");
        let path = dir.path("p.duckdb");
        {
            let conn = Connection::open(&path).unwrap();
            conn.execute_batch(LEGACY).unwrap();
            // Breaks a constraint of the clean schema: a skip with a score.
            conn.execute_batch("INSERT INTO attempts VALUES ('two-sum', 9, 'skip', [], 0.5, 0)")
                .unwrap();
        }
        let mut conn = Connection::open(&path).unwrap();
        assert!(migrate(&mut conn).is_err());
        assert_eq!(shape(&conn).unwrap(), Shape::Unversioned);
        let rows: i64 = conn
            .query_row("SELECT count(*) FROM attempts", [], |r| r.get(0))
            .unwrap();
        assert_eq!(rows, 4);
    }
}
