//! The learner's own problem lists (`migrations/0006_user_lists.sql`). The server keeps them in
//! memory like plans; every write here runs under `AppState::update_progress`, which is what
//! keeps each slug once per list.

use anyhow::Result;
use duckdb::params;

use super::{Store, UserId};

/// Lists allowed.
pub const MAX_LISTS: usize = 50;
/// Problems one list may hold.
pub const MAX_LIST_PROBLEMS: usize = 1000;

/// A stored list: its id, name and problems in list order.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StoredList {
    pub id: i64,
    pub name: String,
    pub slugs: Vec<String>,
}

impl Store {
    /// Every list, newest first, with its problems in order.
    pub fn lists(&self, user: UserId) -> Result<Vec<StoredList>> {
        self.with(|c| {
            let mut lists: Vec<StoredList> = c
                .prepare_cached(
                    "SELECT id, name FROM user_lists WHERE user_id = ?
                     ORDER BY created_at DESC, id DESC",
                )?
                .query_map([user], |r| {
                    Ok(StoredList {
                        id: r.get(0)?,
                        name: r.get(1)?,
                        slugs: Vec::new(),
                    })
                })?
                .collect::<Result<_, _>>()?;
            let mut items = c.prepare_cached(
                "SELECT p.list_id, p.slug FROM user_list_problems p
                 JOIN user_lists l ON l.id = p.list_id
                 WHERE l.user_id = ? ORDER BY p.list_id, p.position",
            )?;
            let rows = items.query_map([user], |r| {
                Ok((r.get::<_, i64>(0)?, r.get::<_, String>(1)?))
            })?;
            for row in rows {
                let (id, slug) = row?;
                if let Some(list) = lists.iter_mut().find(|l| l.id == id) {
                    list.slugs.push(slug);
                }
            }
            Ok(lists)
        })
    }

    /// Makes a list of `slugs` (checked by the caller: known, each once) at `at`. Returns its
    /// id, or `None` when there are [`MAX_LISTS`] lists already.
    pub fn create_list(
        &self,
        user: UserId,
        name: &str,
        slugs: &[String],
        at: i64,
    ) -> Result<Option<i64>> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let count: i64 = tx.query_row(
            "SELECT count(*) FROM user_lists WHERE user_id = ?",
            [user],
            |r| r.get(0),
        )?;
        if usize::try_from(count).unwrap_or(usize::MAX) >= MAX_LISTS {
            return Ok(None);
        }
        let id: i64 = tx
            .prepare_cached(
                "INSERT INTO user_lists (user_id, name, created_at, updated_at)
                 VALUES ($3, $1, to_timestamp($2 / 1000), to_timestamp($2 / 1000)) RETURNING id",
            )?
            .query_row(params![name, at, user], |r| r.get(0))?;
        insert_problems(&tx, id, slugs)?;
        tx.commit()?;
        Ok(Some(id))
    }

    /// Renames a list, replaces its problems (in the new order), or both; `false` when no
    /// list has the id.
    pub fn change_list(
        &self,
        user: UserId,
        id: i64,
        name: Option<&str>,
        slugs: Option<&[String]>,
        at: i64,
    ) -> Result<bool> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let found: i64 = tx.query_row(
            "SELECT count(*) FROM user_lists WHERE user_id = ? AND id = ?",
            params![user, id],
            |r| r.get(0),
        )?;
        if found == 0 {
            return Ok(false);
        }
        if let Some(name) = name {
            tx.prepare_cached("UPDATE user_lists SET name = ? WHERE user_id = ? AND id = ?")?
                .execute(params![name, user, id])?;
        }
        if let Some(slugs) = slugs {
            tx.prepare_cached("DELETE FROM user_list_problems WHERE list_id = ?")?
                .execute([id])?;
            insert_problems(&tx, id, slugs)?;
        }
        tx.prepare_cached(
            "UPDATE user_lists SET updated_at = to_timestamp(? / 1000) WHERE user_id = ? AND id = ?",
        )?
        .execute(params![at, user, id])?;
        tx.commit()?;
        Ok(true)
    }

    /// Deletes a list and its problems; `false` when no list has the id.
    pub fn delete_list(&self, user: UserId, id: i64) -> Result<bool> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let deleted = tx
            .prepare_cached("DELETE FROM user_lists WHERE user_id = ? AND id = ?")?
            .execute(params![user, id])?;
        if deleted > 0 {
            tx.prepare_cached("DELETE FROM user_list_problems WHERE list_id = ?")?
                .execute([id])?;
        }
        tx.commit()?;
        Ok(deleted > 0)
    }
}

fn insert_problems(tx: &duckdb::Transaction<'_>, id: i64, slugs: &[String]) -> Result<()> {
    let mut insert = tx.prepare_cached(
        "INSERT INTO user_list_problems (list_id, slug, position) VALUES (?, ?, ?)",
    )?;
    for (position, slug) in (0_i64..).zip(slugs) {
        insert.execute(params![id, slug, position])?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const U: UserId = UserId::test(1);
    use crate::db::testing::TempDir;

    fn store() -> (Store, TempDir) {
        let dir = TempDir::new("db-lists");
        let (store, _) =
            Store::open(&dir.path("openleet.duckdb"), &dir.path("missing.duckdb")).unwrap();
        (store, dir)
    }

    fn slugs(names: &[&str]) -> Vec<String> {
        names.iter().map(|&s| s.to_owned()).collect()
    }

    #[test]
    fn creates_renames_reorders_and_deletes_lists() {
        let (store, _dir) = store();
        let first = store
            .create_list(U, "Graphs", &slugs(&["b", "a"]), 1_000)
            .unwrap()
            .expect("created");
        let second = store
            .create_list(U, "Empty", &[], 2_000)
            .unwrap()
            .expect("created");
        let lists = store.lists(U).unwrap();
        assert_eq!(
            lists,
            [
                StoredList {
                    id: second,
                    name: "Empty".into(),
                    slugs: vec![]
                },
                StoredList {
                    id: first,
                    name: "Graphs".into(),
                    slugs: slugs(&["b", "a"])
                },
            ]
        );

        let reordered = slugs(&["a", "c", "b"]);
        assert!(
            store
                .change_list(U, first, Some("Graph drills"), Some(&reordered), 3_000)
                .unwrap()
        );
        assert!(!store.change_list(U, 99, Some("x"), None, 3_000).unwrap());
        let changed = store
            .lists(U)
            .unwrap()
            .into_iter()
            .find(|l| l.id == first)
            .unwrap();
        assert_eq!(
            (changed.name.as_str(), changed.slugs),
            ("Graph drills", reordered)
        );

        assert!(store.delete_list(U, first).unwrap());
        assert!(!store.delete_list(U, first).unwrap());
        assert_eq!(store.lists(U).unwrap().len(), 1);
    }

    #[test]
    fn refuses_a_list_past_the_limit() {
        let (store, _dir) = store();
        for i in 0..MAX_LISTS {
            store
                .create_list(U, &format!("List {i}"), &[], 1_000)
                .unwrap();
        }
        assert_eq!(store.create_list(U, "One more", &[], 2_000).unwrap(), None);
    }
}
