//! Accounts, sessions and server settings (`migrations/0007_accounts.sql`).
//!
//! [`UserId`] values come only from these tables: a handler gets one from a session, never
//! from the request, and every progress query takes one.

use anyhow::Result;
use duckdb::types::{ToSql, ToSqlOutput};
use duckdb::{OptionalExt, params};

use super::Store;

/// An account's id. Only the database makes these, from rows of `users` or `sessions`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct UserId(i64);

impl UserId {
    /// The first admin, who owns the progress from before accounts.
    pub const FIRST_ADMIN: Self = Self(1);

    /// An id for tests, which make users without the database.
    #[cfg(test)]
    pub const fn test(id: i64) -> Self {
        Self(id)
    }
}

impl std::fmt::Display for UserId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "user {}", self.0)
    }
}

impl ToSql for UserId {
    fn to_sql(&self) -> duckdb::Result<ToSqlOutput<'_>> {
        self.0.to_sql()
    }
}

/// An account as the server keeps it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct User {
    pub id: UserId,
    pub email: String,
    pub admin: bool,
}

/// An account with its password hash, for signing in.
pub struct Credentials {
    pub user: User,
    pub password_hash: String,
}

/// A stored session.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct StoredSession {
    pub token_hash: [u8; 32],
    pub user: UserId,
    pub expires_at: i64,
}

/// Why an account could not be made.
#[derive(Debug, PartialEq, Eq)]
pub enum NewUser {
    Created(UserId),
    /// The email has an account.
    Taken,
    /// The first admin exists (a setup sign-up came too late).
    AdminExists,
}

/// The tables a user's progress lives in, each with a `user_id` column. Deleting an account
/// deletes its rows from each; `user_list_problems` goes through `user_lists`.
const PROGRESS_TABLES: [&str; 7] = [
    "attempts",
    "daily_scores",
    "notes",
    "drafts",
    "submissions",
    "plans",
    "user_lists",
];

fn user_from_row(r: &duckdb::Row<'_>) -> duckdb::Result<User> {
    Ok(User {
        id: UserId(r.get(0)?),
        email: r.get(1)?,
        admin: r.get(2)?,
    })
}

impl Store {
    /// Makes an account. `first_admin` makes user 1, the admin who owns the progress from
    /// before accounts; that works once.
    pub fn create_user(
        &self,
        email: &str,
        password_hash: &str,
        first_admin: bool,
        at: i64,
    ) -> Result<NewUser> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let taken: i64 = tx
            .prepare_cached("SELECT count(*) FROM users WHERE email = ?")?
            .query_row([email], |r| r.get(0))?;
        if taken > 0 {
            return Ok(NewUser::Taken);
        }
        let id: i64 = if first_admin {
            let exists: i64 = tx.query_row(
                "SELECT count(*) FROM users WHERE id = ?",
                [UserId::FIRST_ADMIN],
                |r| r.get(0),
            )?;
            if exists > 0 {
                return Ok(NewUser::AdminExists);
            }
            tx.prepare_cached(
                "INSERT INTO users (id, email, password_hash, admin, created_at,
                    password_changed_at)
                 VALUES ($1, $2, $3, true, to_timestamp($4 / 1000), to_timestamp($4 / 1000))
                 RETURNING id",
            )?
            .query_row(
                params![UserId::FIRST_ADMIN, email, password_hash, at],
                |r| r.get(0),
            )?
        } else {
            tx.prepare_cached(
                "INSERT INTO users (email, password_hash, admin, created_at, password_changed_at)
                 VALUES ($1, $2, false, to_timestamp($3 / 1000), to_timestamp($3 / 1000))
                 RETURNING id",
            )?
            .query_row(params![email, password_hash, at], |r| r.get(0))?
        };
        tx.commit()?;
        Ok(NewUser::Created(UserId(id)))
    }

    /// The account with this email and its password hash.
    pub fn credentials(&self, email: &str) -> Result<Option<Credentials>> {
        self.with(|c| {
            c.prepare_cached("SELECT id, email, admin, password_hash FROM users WHERE email = ?")?
                .query_row([email], |r| {
                    Ok(Credentials {
                        user: user_from_row(r)?,
                        password_hash: r.get(3)?,
                    })
                })
                .optional()
        })
    }

    /// An account's password hash.
    pub fn password_hash(&self, user: UserId) -> Result<Option<String>> {
        self.with(|c| {
            c.prepare_cached("SELECT password_hash FROM users WHERE id = ?")?
                .query_row([user], |r| r.get(0))
                .optional()
        })
    }

    /// Every account, by id.
    pub fn users(&self) -> Result<Vec<User>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached("SELECT id, email, admin FROM users ORDER BY id")?;
            let rows = stmt.query_map([], user_from_row)?;
            rows.collect()
        })
    }

    /// Whether the first admin has an account.
    pub fn has_first_admin(&self) -> Result<bool> {
        self.with(|c| {
            c.query_row(
                "SELECT count(*) > 0 FROM users WHERE id = ?",
                [UserId::FIRST_ADMIN],
                |r| r.get(0),
            )
        })
    }

    /// Sets a new password and ends every session of the account but `keep`.
    pub fn set_password(
        &self,
        user: UserId,
        password_hash: &str,
        keep: &[u8; 32],
        at: i64,
    ) -> Result<()> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        tx.prepare_cached(
            "UPDATE users SET password_hash = ?, password_changed_at = to_timestamp(? / 1000)
             WHERE id = ?",
        )?
        .execute(params![password_hash, at, user])?;
        tx.prepare_cached("DELETE FROM sessions WHERE user_id = ? AND token_hash <> ?")?
            .execute(params![user, keep.as_slice()])?;
        tx.commit()?;
        Ok(())
    }

    /// Deletes an account with all its progress and sessions, in one transaction.
    pub fn delete_user(&self, user: UserId) -> Result<()> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        tx.prepare_cached(
            "DELETE FROM user_list_problems
             WHERE list_id IN (SELECT id FROM user_lists WHERE user_id = ?)",
        )?
        .execute([user])?;
        for table in PROGRESS_TABLES {
            tx.execute(&format!("DELETE FROM {table} WHERE user_id = ?"), [user])?;
        }
        tx.prepare_cached("DELETE FROM sessions WHERE user_id = ?")?
            .execute([user])?;
        tx.prepare_cached("DELETE FROM users WHERE id = ?")?
            .execute([user])?;
        tx.commit()?;
        Ok(())
    }

    /// Every session that has not expired at `now`; expired ones are deleted.
    pub fn sessions(&self, now: i64) -> Result<Vec<StoredSession>> {
        self.with(|c| {
            c.prepare_cached("DELETE FROM sessions WHERE expires_at <= to_timestamp(? / 1000)")?
                .execute([now])?;
            let mut stmt =
                c.prepare_cached("SELECT token_hash, user_id, epoch_ms(expires_at) FROM sessions")?;
            let rows = stmt.query_map([], |r| {
                let hash: Vec<u8> = r.get(0)?;
                Ok((hash, r.get::<_, i64>(1)?, r.get::<_, i64>(2)?))
            })?;
            let mut sessions = Vec::new();
            for row in rows {
                let (hash, user, expires_at) = row?;
                if let Ok(token_hash) = <[u8; 32]>::try_from(hash) {
                    sessions.push(StoredSession {
                        token_hash,
                        user: UserId(user),
                        expires_at,
                    });
                }
            }
            Ok(sessions)
        })
    }

    /// Stores a new session and ends the account's oldest beyond `keep`; returns the hashes
    /// of the account's sessions that remain.
    pub fn insert_session(
        &self,
        session: &StoredSession,
        at: i64,
        keep: usize,
    ) -> Result<Vec<[u8; 32]>> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        tx.prepare_cached(
            "INSERT INTO sessions (token_hash, user_id, created_at, expires_at)
             VALUES (?, ?, to_timestamp(? / 1000), to_timestamp(? / 1000))",
        )?
        .execute(params![
            session.token_hash.as_slice(),
            session.user,
            at,
            session.expires_at
        ])?;
        // Newest first; the ones past `keep` end. (One DELETE with `NOT IN (... LIMIT ?)`
        // crashes DuckDB 2.0 after some deletes and updates of this table.)
        let mut hashes: Vec<Vec<u8>> = tx
            .prepare_cached(
                "SELECT token_hash FROM sessions WHERE user_id = ?
                 ORDER BY created_at DESC, expires_at DESC",
            )?
            .query_map([session.user], |r| r.get(0))?
            .collect::<duckdb::Result<_>>()?;
        for ended in hashes.drain(keep.min(hashes.len())..) {
            tx.prepare_cached("DELETE FROM sessions WHERE token_hash = ?")?
                .execute([ended])?;
        }
        tx.commit()?;
        Ok(hashes
            .into_iter()
            .filter_map(|h| <[u8; 32]>::try_from(h).ok())
            .collect())
    }

    pub fn extend_session(&self, token_hash: &[u8; 32], expires_at: i64) -> Result<()> {
        self.with(|c| {
            c.prepare_cached(
                "UPDATE sessions SET expires_at = to_timestamp(? / 1000) WHERE token_hash = ?",
            )?
            .execute(params![expires_at, token_hash.as_slice()])
            .map(drop)
        })
    }

    pub fn delete_session(&self, token_hash: &[u8; 32]) -> Result<()> {
        self.with(|c| {
            c.prepare_cached("DELETE FROM sessions WHERE token_hash = ?")?
                .execute([token_hash.as_slice()])
                .map(drop)
        })
    }

    /// How many rows of progress the account has, in every table (for tests).
    #[cfg(test)]
    pub fn rows_of(&self, user: UserId) -> Result<i64> {
        let mut total = 0;
        for table in PROGRESS_TABLES {
            total += self.with(|c| {
                c.query_row(
                    &format!("SELECT count(*) FROM {table} WHERE user_id = ?"),
                    [user],
                    |r| r.get::<_, i64>(0),
                )
            })?;
        }
        total += self.with(|c| {
            c.query_row(
                "SELECT count(*) FROM user_list_problems
                 WHERE list_id NOT IN (SELECT id FROM user_lists)",
                [],
                |r| r.get::<_, i64>(0),
            )
        })?;
        total += self.with(|c| {
            c.query_row(
                "SELECT count(*) FROM sessions WHERE user_id = ?",
                [user],
                |r| r.get::<_, i64>(0),
            )
        })?;
        Ok(total)
    }

    /// Whether anyone can make an account.
    pub fn signups_open(&self) -> Result<bool> {
        self.with(|c| c.query_row("SELECT signups_open FROM settings", [], |r| r.get(0)))
    }

    pub fn set_signups_open(&self, open: bool) -> Result<()> {
        self.with(|c| {
            c.prepare_cached("UPDATE settings SET signups_open = ?")?
                .execute([open])
                .map(drop)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    const HASH: &str = "$argon2id$v=19$m=19456,t=2,p=1$c2FsdA$aGFzaA";

    fn store() -> (Store, TempDir) {
        let dir = TempDir::new("db-accounts");
        let (store, _) =
            Store::open(&dir.path("openleet.duckdb"), &dir.path("missing.duckdb")).unwrap();
        (store, dir)
    }

    #[test]
    fn the_first_admin_is_user_1_and_others_follow() {
        let (store, _dir) = store();
        assert!(!store.has_first_admin().unwrap());
        let other = store.create_user("b@example.com", HASH, false, 1).unwrap();
        assert_eq!(other, NewUser::Created(UserId(2)));
        assert_eq!(
            store.create_user("a@example.com", HASH, true, 2).unwrap(),
            NewUser::Created(UserId::FIRST_ADMIN)
        );
        assert!(store.has_first_admin().unwrap());
        assert_eq!(
            store.create_user("c@example.com", HASH, true, 3).unwrap(),
            NewUser::AdminExists
        );
        assert_eq!(
            store.create_user("b@example.com", HASH, false, 4).unwrap(),
            NewUser::Taken
        );
        let users = store.users().unwrap();
        assert_eq!(
            users.iter().map(|u| (u.id, u.admin)).collect::<Vec<_>>(),
            [(UserId(1), true), (UserId(2), false)]
        );
        let found = store.credentials("a@example.com").unwrap().unwrap();
        assert_eq!(found.user.id, UserId(1));
        assert!(store.credentials("nobody@example.com").unwrap().is_none());
        // Only Argon2id hashes are stored.
        assert!(
            store
                .create_user("d@example.com", "plain", false, 5)
                .is_err()
        );
    }

    #[test]
    fn sessions_expire_and_a_new_password_ends_the_others() {
        let (store, _dir) = store();
        let NewUser::Created(user) = store.create_user("a@example.com", HASH, false, 1).unwrap()
        else {
            panic!("created");
        };
        let session = |byte: u8, expires_at| StoredSession {
            token_hash: [byte; 32],
            user,
            expires_at,
        };
        store.insert_session(&session(1, 1_000_000), 1, 20).unwrap();
        store.insert_session(&session(2, 1_000_000), 1, 20).unwrap();
        store.insert_session(&session(3, 10), 1, 20).unwrap();
        assert_eq!(
            store.sessions(100).unwrap().len(),
            2,
            "the expired one goes"
        );
        store.set_password(user, HASH, &[1; 32], 200).unwrap();
        assert_eq!(store.sessions(100).unwrap(), [session(1, 1_000_000)]);
        store.extend_session(&[1; 32], 2_000_000).unwrap();
        assert_eq!(store.sessions(100).unwrap()[0].expires_at, 2_000_000);
        store.delete_session(&[1; 32]).unwrap();
        assert!(store.sessions(100).unwrap().is_empty());
        // Past the limit, the oldest sessions end.
        for byte in 10..15 {
            store
                .insert_session(&session(byte, 1_000_000), i64::from(byte), 3)
                .unwrap();
        }
        let mut kept = store
            .insert_session(&session(15, 1_000_000), 15, 3)
            .unwrap();
        kept.sort_unstable();
        assert_eq!(kept, [[13; 32], [14; 32], [15; 32]]);
    }

    #[test]
    fn deleting_an_account_deletes_its_progress_only() {
        let (store, _dir) = store();
        let make = |email| match store.create_user(email, HASH, false, 1).unwrap() {
            NewUser::Created(id) => id,
            other => panic!("{other:?}"),
        };
        let (a, b) = (make("a@example.com"), make("b@example.com"));
        for user in [a, b] {
            store.save_note(user, "two-sum", "mine", 1).unwrap();
            store.save_draft(user, "two-sum", "code", 1).unwrap();
            store
                .create_list(user, "Mine", &["two-sum".to_owned()], 1)
                .unwrap();
            store
                .insert_session(
                    &StoredSession {
                        token_hash: [u8::try_from(user.0).unwrap(); 32],
                        user,
                        expires_at: 1_000_000,
                    },
                    1,
                    20,
                )
                .unwrap();
        }
        store.delete_user(a).unwrap();
        assert!(store.notes(a).unwrap().is_empty());
        assert_eq!(store.notes(b).unwrap().len(), 1);
        assert!(store.lists(a).unwrap().is_empty());
        assert_eq!(store.lists(b).unwrap()[0].slugs, ["two-sum"]);
        assert_eq!(
            store.draft(b, "two-sum").unwrap().code.as_deref(),
            Some("code")
        );
        let sessions = store.sessions(0).unwrap();
        assert_eq!(sessions.len(), 1);
        assert_eq!(sessions[0].user, b);
        assert!(store.credentials("a@example.com").unwrap().is_none());
    }

    #[test]
    fn signups_start_open_and_can_close() {
        let (store, _dir) = store();
        assert!(store.signups_open().unwrap());
        store.set_signups_open(false).unwrap();
        assert!(!store.signups_open().unwrap());
    }
}
