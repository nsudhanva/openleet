//! Practice plans the learner used: pinned ones, and the most recent others
//! (`migrations/0002_plans.sql`). The server keeps them in memory like notes; every write
//! here runs under `AppState::update_progress`, which is what keeps one row per plan.

use anyhow::Result;
use duckdb::{OptionalExt, params};

use super::Store;

/// Unpinned plans kept; using another drops the least recently used.
pub const MAX_RECENT_PLANS: usize = 8;
/// Pinned plans allowed.
pub const MAX_PINNED_PLANS: usize = 50;

/// The values that make a plan, in the API's spellings (see `openleet::plan::PlanView`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PlanKey<'a> {
    pub company: &'a str,
    pub period: &'a str,
    pub topic: Option<&'a str>,
    pub difficulty: Option<&'a str>,
    pub status: &'a str,
    pub order: &'a str,
}

/// A stored plan.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SavedPlan {
    pub id: i64,
    pub company: String,
    pub period: String,
    pub topic: Option<String>,
    pub difficulty: Option<String>,
    pub status: String,
    pub order: String,
    pub name: Option<String>,
    pub pinned: bool,
    /// When it was last used, Unix milliseconds.
    pub used_at: i64,
}

/// A change to a stored plan: `name` is `Some(None)` to drop the name.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct PlanChange {
    pub name: Option<Option<String>>,
    pub pinned: Option<bool>,
}

/// What [`Store::change_plan`] did.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Changed {
    Done,
    /// No plan has the id.
    Missing,
    /// Pinning it would pass [`MAX_PINNED_PLANS`].
    TooManyPinned,
}

/// Drops the unpinned plans beyond the [`MAX_RECENT_PLANS`] most recently used.
const PRUNE: &str = "DELETE FROM plans WHERE NOT pinned AND id NOT IN (
    SELECT id FROM plans WHERE NOT pinned ORDER BY used_at DESC, id DESC LIMIT ?)";

impl Store {
    /// Every stored plan: pinned first, then by when it was last used, newest first.
    pub fn plans(&self) -> Result<Vec<SavedPlan>> {
        self.with(|c| {
            let mut stmt = c.prepare_cached(
                "SELECT id, company, period, topic, difficulty, status::VARCHAR,
                    sort_order::VARCHAR, name, pinned, epoch_ms(used_at)
                 FROM plans ORDER BY pinned DESC, used_at DESC, id DESC",
            )?;
            let rows = stmt.query_map([], |r| {
                Ok(SavedPlan {
                    id: r.get(0)?,
                    company: r.get(1)?,
                    period: r.get(2)?,
                    topic: r.get(3)?,
                    difficulty: r.get(4)?,
                    status: r.get(5)?,
                    order: r.get(6)?,
                    name: r.get(7)?,
                    pinned: r.get(8)?,
                    used_at: r.get(9)?,
                })
            })?;
            rows.collect()
        })
    }

    /// Records that a plan was used at `at`: the row with exactly these values (NULL
    /// matching NULL) is touched, or a new one inserted; then the oldest unpinned plans past
    /// [`MAX_RECENT_PLANS`] go. Returns the plan's id. One row per plan holds only while
    /// writes are serialized, as `AppState::update_progress` does.
    pub fn use_plan(&self, key: &PlanKey<'_>, at: i64) -> Result<i64> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let found: Option<i64> = tx
            .prepare_cached(
                "SELECT id FROM plans WHERE company = ? AND period = ?
                    AND topic IS NOT DISTINCT FROM ? AND difficulty IS NOT DISTINCT FROM ?
                    AND status = ? AND sort_order = ?",
            )?
            .query_row(
                params![
                    key.company,
                    key.period,
                    key.topic,
                    key.difficulty,
                    key.status,
                    key.order
                ],
                |r| r.get(0),
            )
            .optional()?;
        let id = match found {
            Some(id) => {
                tx.prepare_cached("UPDATE plans SET used_at = to_timestamp(? / 1000) WHERE id = ?")?
                    .execute(params![at, id])?;
                id
            }
            None => tx
                .prepare_cached(
                    "INSERT INTO plans (company, period, topic, difficulty, status, sort_order,
                        created_at, used_at)
                     VALUES ($1, $2, $3, $4, $5, $6, to_timestamp($7 / 1000), to_timestamp($7 / 1000))
                     RETURNING id",
                )?
                .query_row(
                    params![
                        key.company,
                        key.period,
                        key.topic,
                        key.difficulty,
                        key.status,
                        key.order,
                        at
                    ],
                    |r| r.get(0),
                )?,
        };
        tx.prepare_cached(PRUNE)?.execute([MAX_RECENT_PLANS])?;
        tx.commit()?;
        Ok(id)
    }

    /// Renames, pins or unpins a plan. Unpinning counts as using it, so it heads the recent
    /// plans instead of being dropped at once.
    pub fn change_plan(&self, id: i64, change: &PlanChange, at: i64) -> Result<Changed> {
        let mut conn = self.conn.lock();
        let tx = conn.transaction()?;
        let pinned: Option<bool> = tx
            .prepare_cached("SELECT pinned FROM plans WHERE id = ?")?
            .query_row([id], |r| r.get(0))
            .optional()?;
        let Some(was_pinned) = pinned else {
            return Ok(Changed::Missing);
        };
        if change.pinned == Some(true) && !was_pinned {
            let pinned: i64 =
                tx.query_row("SELECT count(*) FROM plans WHERE pinned", [], |r| r.get(0))?;
            if usize::try_from(pinned).unwrap_or(usize::MAX) >= MAX_PINNED_PLANS {
                return Ok(Changed::TooManyPinned);
            }
        }
        if let Some(name) = &change.name {
            tx.prepare_cached("UPDATE plans SET name = ? WHERE id = ?")?
                .execute(params![name, id])?;
        }
        if let Some(pinned) = change.pinned {
            tx.prepare_cached(
                "UPDATE plans SET pinned = $1,
                    used_at = CASE WHEN $1 THEN used_at ELSE to_timestamp($2 / 1000) END
                 WHERE id = $3",
            )?
            .execute(params![pinned, at, id])?;
            tx.prepare_cached(PRUNE)?.execute([MAX_RECENT_PLANS])?;
        }
        tx.commit()?;
        Ok(Changed::Done)
    }

    /// Forgets a plan; `false` when no plan has the id.
    pub fn delete_plan(&self, id: i64) -> Result<bool> {
        self.with(|c| {
            c.prepare_cached("DELETE FROM plans WHERE id = ?")?
                .execute([id])
                .map(|n| n > 0)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    fn store() -> (Store, TempDir) {
        let dir = TempDir::new("db-plans");
        let (store, _) =
            Store::open(&dir.path("openleet.duckdb"), &dir.path("missing.duckdb")).unwrap();
        (store, dir)
    }

    const GOOGLE: PlanKey<'static> = PlanKey {
        company: "google",
        period: "6m",
        topic: None,
        difficulty: None,
        status: "unsolved",
        order: "rank",
    };

    #[test]
    fn keeps_one_row_per_plan_matching_null_filters() {
        let (store, _dir) = store();
        let first = store.use_plan(&GOOGLE, 1_000).unwrap();
        assert_eq!(store.use_plan(&GOOGLE, 2_000).unwrap(), first);
        let graph = PlanKey {
            topic: Some("Graph"),
            ..GOOGLE
        };
        let second = store.use_plan(&graph, 3_000).unwrap();
        assert_ne!(second, first);
        assert_eq!(store.use_plan(&graph, 4_000).unwrap(), second);
        let hard = PlanKey {
            difficulty: Some("Hard"),
            order: "random",
            ..graph
        };
        let third = store.use_plan(&hard, 5_000).unwrap();
        let plans = store.plans().unwrap();
        assert_eq!(
            plans.iter().map(|p| (p.id, p.used_at)).collect::<Vec<_>>(),
            [(third, 5_000), (second, 4_000), (first, 2_000)]
        );
        assert_eq!(
            (plans[0].difficulty.as_deref(), plans[0].order.as_str()),
            (Some("Hard"), "random")
        );
    }

    #[test]
    fn keeps_the_recent_unpinned_plans_and_every_pinned_one() {
        let (store, _dir) = store();
        let topics = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
        let ids: Vec<i64> = (0_i64..)
            .zip(topics)
            .map(|(at, topic)| {
                let key = PlanKey {
                    topic: Some(topic),
                    ..GOOGLE
                };
                store.use_plan(&key, at).unwrap()
            })
            .collect();
        // The first two went when the ninth and tenth were used.
        let kept: Vec<i64> = store.plans().unwrap().iter().map(|p| p.id).collect();
        assert_eq!(kept.len(), MAX_RECENT_PLANS);
        assert!(!kept.contains(&ids[0]) && !kept.contains(&ids[1]));

        // A pinned plan is kept apart from the recent ones, named or not.
        let pin = PlanChange {
            pinned: Some(true),
            name: Some(Some("Graphs".into())),
        };
        assert_eq!(store.change_plan(ids[2], &pin, 20).unwrap(), Changed::Done);
        store.use_plan(&GOOGLE, 30).unwrap();
        let plans = store.plans().unwrap();
        assert_eq!(plans[0].id, ids[2]);
        assert_eq!(
            (plans[0].pinned, plans[0].name.as_deref()),
            (true, Some("Graphs"))
        );
        assert_eq!(plans.len(), MAX_RECENT_PLANS + 1);

        // Unpinned, it heads the recent plans; the name can be dropped.
        let unpin = PlanChange {
            pinned: Some(false),
            name: Some(None),
        };
        assert_eq!(
            store.change_plan(ids[2], &unpin, 40).unwrap(),
            Changed::Done
        );
        let plans = store.plans().unwrap();
        assert_eq!((plans[0].id, plans[0].used_at), (ids[2], 40));
        assert_eq!((plans[0].pinned, plans[0].name.as_deref()), (false, None));
        assert_eq!(plans.len(), MAX_RECENT_PLANS);

        assert_eq!(
            store.change_plan(999, &PlanChange::default(), 0).unwrap(),
            Changed::Missing
        );
        assert!(store.delete_plan(ids[2]).unwrap());
        assert!(!store.delete_plan(ids[2]).unwrap());
    }

    #[test]
    fn refuses_more_pinned_plans_than_allowed() {
        let (store, _dir) = store();
        let pin = PlanChange {
            pinned: Some(true),
            name: None,
        };
        let names: Vec<String> = (0..=MAX_PINNED_PLANS).map(|i| format!("t{i}")).collect();
        let mut last = Changed::Done;
        for (at, name) in (0_i64..).zip(&names) {
            let key = PlanKey {
                topic: Some(name),
                ..GOOGLE
            };
            let id = store.use_plan(&key, at).unwrap();
            last = store.change_plan(id, &pin, at).unwrap();
        }
        assert_eq!(last, Changed::TooManyPinned);
        let pinned = store.plans().unwrap().iter().filter(|p| p.pinned).count();
        assert_eq!(pinned, MAX_PINNED_PLANS);
    }
}
