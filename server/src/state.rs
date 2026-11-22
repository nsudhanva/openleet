//! Shared server state: static content, accounts, each active account's progress in memory,
//! storage and the judge.

use std::collections::HashMap;
use std::sync::Arc;

use anyhow::Result;
use std::sync::atomic::{AtomicBool, Ordering};

use parking_lot::{Mutex, RwLock, RwLockReadGuard, RwLockWriteGuard};

use openleet::coding::CodingLog;
use openleet::content::Content;
use openleet::insights;
use openleet::model::{Attempt, CompanyFilter, Problem};
use openleet::plan::Marks;
use openleet::scheduler::{CardStates, card_states, record_attempt};
use openleet::scorer::{ScoreReport, local_zone, score_report};
use openleet::service;
use openleet::user_lists::{UserList, UserLists};
use openleet_proto::Verdict;

use crate::acme::CertificateSlot;
use crate::auth::Auth;
use crate::db::{SavedPlan, Store, StoredList, UserId};
use crate::error::{ApiError, ApiResult};
use crate::judge::Judge;

/// The stored lists, resolved against the content.
pub fn user_lists(content: &Content, stored: Vec<StoredList>) -> UserLists {
    UserLists::new(
        stored
            .into_iter()
            .map(|list| UserList::new(content, list.id, list.name, list.slugs))
            .collect(),
    )
}

/// Everything derived from one account's attempt log, kept in memory so reads never touch the
/// disk.
pub struct Progress {
    /// The attempt log, oldest first.
    pub attempts: Vec<Attempt>,
    /// Card state per slug, replayed from `attempts`.
    pub states: CardStates,
    /// Your answer per slug.
    pub notes: HashMap<String, String>,
    /// Every judged submission, aggregated per problem (solved, tried, shaky, ...).
    pub coding: CodingLog,
    /// Practice plans used, as [`Store::plans`] lists them; replaced after every plan write.
    pub plans: Vec<SavedPlan>,
    /// The learner's own lists, as [`Store::lists`] lists them; replaced after every list
    /// write.
    pub lists: UserLists,
    /// Reports per company, computed on first read after the log changed.
    reports: HashMap<CompanyFilter, Arc<ScoreReport>>,
}

impl Progress {
    /// Replays the attempt log into card states.
    pub fn new(
        attempts: Vec<Attempt>,
        notes: HashMap<String, String>,
        coding: CodingLog,
        plans: Vec<SavedPlan>,
        lists: UserLists,
    ) -> Self {
        let states = card_states(&attempts);
        Self {
            attempts,
            states,
            notes,
            coding,
            plans,
            lists,
            reports: HashMap::new(),
        }
    }

    /// What the learner did in the judge, for plans.
    pub const fn marks(&self) -> Marks<'_> {
        &self.coding
    }

    /// Records a new attempt.
    pub fn push(&mut self, attempt: Attempt) {
        record_attempt(&mut self.states, &attempt);
        self.attempts.push(attempt);
        self.reports.clear();
    }

    /// Records a judged submission.
    pub fn record_submission(&mut self, slug: &str, at: i64, verdict: Verdict) {
        self.coding.record(slug, at, verdict);
        self.reports.clear();
    }

    /// Forgets one problem's attempts, or every attempt.
    pub fn clear(&mut self, slug: Option<&str>) {
        match slug {
            Some(slug) => self.attempts.retain(|a| a.slug != slug),
            None => self.attempts.clear(),
        }
        self.states = card_states(&self.attempts);
        self.reports.clear();
    }

    /// Drops every cached report.
    pub fn invalidate_reports(&mut self) {
        self.reports.clear();
    }

    /// What the learner did, for the report and the insights.
    pub fn learner(&self) -> insights::Learner<'_> {
        insights::Learner {
            attempts: &self.attempts,
            states: &self.states,
            coding: &self.coding,
        }
    }

    /// A company's report, computed only on the first read after the logs changed.
    fn report(&mut self, content: &Content, company: CompanyFilter, now: i64) -> Arc<ScoreReport> {
        if let Some(report) = self.reports.get(&company) {
            return Arc::clone(report);
        }
        let report = Arc::new(score_report(
            content,
            company,
            self.learner(),
            now,
            &local_zone(),
        ));
        self.reports.insert(company, Arc::clone(&report));
        report
    }
}

/// One account's progress in memory, and the lock that orders its writes.
pub struct Learner {
    pub user: UserId,
    pub progress: RwLock<Progress>,
    /// Serializes the account's durable writes with publication to `progress`.
    updates: Mutex<()>,
    /// Set once the account is deleted; later writes fail instead of leaving rows behind.
    closed: AtomicBool,
}

impl Learner {
    fn new(user: UserId, progress: Progress) -> Self {
        Self {
            user,
            progress: RwLock::new(progress),
            updates: Mutex::new(()),
            closed: AtomicBool::new(false),
        }
    }

    /// Loads an account's progress from the database.
    fn load(store: &Store, content: &Content, user: UserId) -> Result<Self> {
        let progress = Progress::new(
            store.attempts(user)?,
            store.notes(user)?,
            store.coding_log(user)?,
            store.plans(user)?,
            user_lists(content, store.lists(user)?),
        );
        Ok(Self::new(user, progress))
    }

    /// A company's report and the progress it was computed from, read-locked. Only a report
    /// missing from the cache takes the write lock, to compute it.
    pub fn report(
        &self,
        content: &Content,
        company: CompanyFilter,
        now: i64,
    ) -> (RwLockReadGuard<'_, Progress>, Arc<ScoreReport>) {
        let progress = self.progress.read();
        if let Some(report) = progress.reports.get(&company).cloned() {
            return (progress, report);
        }
        drop(progress);
        let mut progress = self.progress.write();
        let report = progress.report(content, company, now);
        (RwLockWriteGuard::downgrade(progress), report)
    }
}

/// Accounts whose progress stays in memory; the least recently used beyond this are dropped
/// once no request holds them, and loaded again when next needed.
const CACHED_LEARNERS: usize = 64;

/// The progress of recently active accounts.
#[derive(Default)]
pub struct Learners {
    /// Each account's progress and when it was last asked for (a counter).
    cache: Mutex<HashMap<UserId, (Arc<Learner>, u64)>>,
    clock: std::sync::atomic::AtomicU64,
}

impl Learners {
    fn get(&self, user: UserId) -> Option<Arc<Learner>> {
        let tick = self.clock.fetch_add(1, Ordering::Relaxed);
        let mut cache = self.cache.lock();
        let (learner, used) = cache.get_mut(&user)?;
        *used = tick;
        Some(Arc::clone(learner))
    }

    /// Caches a loaded account, unless another request cached it first (that one wins, so an
    /// account never has two copies in memory). Then drops the least recently used accounts
    /// past [`CACHED_LEARNERS`] that no request holds.
    fn insert(&self, learner: Learner) -> Arc<Learner> {
        let tick = self.clock.fetch_add(1, Ordering::Relaxed);
        let mut cache = self.cache.lock();
        let learner = Arc::clone(
            &cache
                .entry(learner.user)
                .or_insert_with(|| (Arc::new(learner), tick))
                .0,
        );
        if cache.len() > CACHED_LEARNERS {
            let mut idle: Vec<(u64, UserId)> = cache
                .iter()
                .filter(|(_, (l, _))| Arc::strong_count(l) == 1)
                .map(|(id, (_, used))| (*used, *id))
                .collect();
            idle.sort_unstable();
            let excess = cache.len() - CACHED_LEARNERS;
            for (_, id) in idle.into_iter().take(excess) {
                cache.remove(&id);
            }
        }
        learner
    }

    fn remove(&self, user: UserId) {
        self.cache.lock().remove(&user);
    }

    /// Every cached account.
    fn all(&self) -> Vec<Arc<Learner>> {
        self.cache
            .lock()
            .values()
            .map(|(l, _)| Arc::clone(l))
            .collect()
    }
}

/// Everything the handlers share.
pub struct AppState {
    pub content: Content,
    /// `GET /api/companies`, ready to send, and its ETag.
    pub companies: (axum::body::Bytes, axum::http::HeaderValue),
    /// The running release, for `GET /api/version`.
    pub revision: String,
    /// The deploy webhook; `None` when `DEPLOY_SECRET` is unset.
    pub deploy: Option<crate::deploy::Deploy>,
    pub store: Store,
    pub judge: Judge,
    pub auth: Auth,
    /// Each active account's progress; reach it with [`AppState::learner`].
    learners: Learners,
    /// Held shared by every progress write and exclusively by an account's deletion, so no
    /// write that checked the account lands after its rows are deleted.
    deletions: RwLock<()>,
    /// The HTTPS certificate in use, for `GET /api/health`.
    pub certificate: CertificateSlot,
}

/// The state handed to every handler.
pub type Shared = Arc<AppState>;

/// The current time in Unix milliseconds.
pub fn now_ms() -> i64 {
    jiff::Timestamp::now().as_millisecond()
}

impl AppState {
    pub fn new(
        content: Content,
        revision: String,
        deploy: Option<crate::deploy::Deploy>,
        store: Store,
        judge: Judge,
        auth: Auth,
        certificate: CertificateSlot,
    ) -> Self {
        Self {
            companies: crate::api::companies_response(&content),
            content,
            revision,
            deploy,
            store,
            judge,
            auth,
            learners: Learners::default(),
            deletions: RwLock::new(()),
            certificate,
        }
    }

    /// The problem with this slug, or a 404.
    pub fn problem(&self, slug: &str) -> ApiResult<&Problem> {
        Ok(service::problem_of(&self.content, slug)?)
    }

    /// An account's progress, from memory, or loaded from the database first.
    pub async fn learner(self: &Arc<Self>, user: UserId) -> ApiResult<Arc<Learner>> {
        if self.auth.is_deleted(user) {
            return Err(ApiError::SignIn);
        }
        if let Some(learner) = self.learners.get(user) {
            return Ok(learner);
        }
        let state = Arc::clone(self);
        let loaded = self
            .db(move |store| Learner::load(store, &state.content, user))
            .await?;
        Ok(self.learners.insert(loaded))
    }

    /// Runs storage work for a known problem (else a 404), handing it the problem's slug.
    pub async fn db_for<T: Send + 'static>(
        self: &Arc<Self>,
        slug: &str,
        work: impl FnOnce(&Store, &str) -> Result<T> + Send + 'static,
    ) -> ApiResult<T> {
        let slug = self.problem(slug)?.slug.clone();
        self.db(move |store| work(store, &slug)).await
    }

    /// Runs blocking storage work off the async workers.
    pub async fn db<T: Send + 'static>(
        self: &Arc<Self>,
        work: impl FnOnce(&Store) -> Result<T> + Send + 'static,
    ) -> ApiResult<T> {
        let state = Arc::clone(self);
        tokio::task::spawn_blocking(move || work(&state.store))
            .await
            .map_err(|e| ApiError::Internal(e.into()))?
            .map_err(ApiError::Internal)
    }

    /// Finishes a durable write to one account's progress and its cache update together, even
    /// if the HTTP request is cancelled. Writes of one account run one at a time; the cache
    /// lock is only held when publishing, so reads need not wait on IO.
    pub async fn update_progress<T: Send + 'static>(
        self: &Arc<Self>,
        learner: &Arc<Learner>,
        work: impl FnOnce(&Self, &Learner) -> Result<T> + Send + 'static,
    ) -> ApiResult<T> {
        let state = Arc::clone(self);
        let learner = Arc::clone(learner);
        tokio::task::spawn_blocking(move || {
            let _update = learner.updates.lock();
            let _deletions = state.deletions.read();
            if learner.closed.load(Ordering::Acquire) || state.auth.is_deleted(learner.user) {
                return Err(ApiError::SignIn);
            }
            work(&state, &learner).map_err(ApiError::Internal)
        })
        .await
        .map_err(|e| ApiError::Internal(e.into()))?
    }

    /// Deletes an account and all its progress. Waits for the account's writes in flight, so
    /// none lands after the delete.
    pub async fn delete_account(self: &Arc<Self>, learner: &Arc<Learner>) -> ApiResult<()> {
        let state = Arc::clone(self);
        let learner = Arc::clone(learner);
        tokio::task::spawn_blocking(move || {
            let _update = learner.updates.lock();
            let _deletions = state.deletions.write();
            learner.closed.store(true, Ordering::Release);
            // First refuse new sessions and writes, then delete what exists.
            state.auth.forget_user(learner.user);
            state.learners.remove(learner.user);
            state.store.delete_user(learner.user)
        })
        .await
        .map_err(|e| ApiError::Internal(e.into()))?
        .map_err(ApiError::Internal)
    }

    /// Drops every cached report, so the next reads see cards fall overdue and days pass.
    pub fn refresh_reports(&self) {
        for learner in self.learners.all() {
            learner.progress.write().invalidate_reports();
        }
    }
}

/// A state over empty content, a new database in `dir` and a judge at `judge`, for tests.
#[cfg(test)]
pub fn test_state(dir: &std::path::Path, judge: &str) -> Shared {
    let none = dir.join("none.json");
    test_state_with(
        dir,
        judge,
        Content::load(&none, &none, &none).expect("content"),
    )
}

/// [`test_state`] over the given content.
#[cfg(test)]
pub fn test_state_with(dir: &std::path::Path, judge: &str, content: Content) -> Shared {
    let none = dir.join("none.json");
    let (store, _) =
        Store::open(&dir.join("openleet.duckdb"), &dir.join("none.duckdb")).expect("database");
    let judge = Judge::load(&none, judge.parse().expect("endpoint")).expect("judge");
    let auth = Auth::load(&store, dir, false, now_ms()).expect("accounts");
    Arc::new(AppState::new(
        content,
        "test".to_owned(),
        None,
        store,
        judge,
        auth,
        CertificateSlot::default(),
    ))
}

/// A new account's id and progress, for tests.
#[cfg(test)]
pub async fn test_learner(state: &Shared, email: &str) -> Arc<Learner> {
    const HASH: &str = "$argon2id$v=19$m=19456,t=2,p=1$c2FsdA$aGFzaA";
    let crate::db::NewUser::Created(user) = state
        .store
        .create_user(email, HASH, false, now_ms())
        .expect("create a user")
    else {
        panic!("{email} has an account");
    };
    state.learner(user).await.expect("load the account")
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    #[tokio::test]
    async fn cached_reports_are_read_without_the_write_lock() {
        let dir = TempDir::new("progress-report");
        let state = test_state(&dir.path(""), "tcp://127.0.0.1:1");
        let learner = test_learner(&state, "a@example.com").await;
        let company = state.content.default_company();
        let (_, computed) = learner.report(&state.content, company, 0);
        // Another reader holds the lock: a cached report must not wait for it.
        let reader = learner.progress.read();
        let (_, cached) = learner.report(&state.content, company, 0);
        drop(reader);
        assert!(Arc::ptr_eq(&computed, &cached));
    }

    #[tokio::test]
    async fn each_account_has_one_copy_in_memory_and_idle_ones_go() {
        let dir = TempDir::new("progress-cache");
        let state = test_state(&dir.path(""), "tcp://127.0.0.1:1");
        let first = test_learner(&state, "a@example.com").await;
        assert!(Arc::ptr_eq(
            &first,
            &state.learner(first.user).await.unwrap()
        ));
        let held = first.user;
        let mut others = Vec::new();
        for i in 0..CACHED_LEARNERS + 5 {
            others.push(
                test_learner(&state, &format!("u{i}@example.com"))
                    .await
                    .user,
            );
        }
        // Held by this test, the first stays; the idle ones beyond the limit went.
        assert_eq!(state.learners.cache.lock().len(), CACHED_LEARNERS);
        assert!(state.learners.get(held).is_some());
        assert!(state.learners.get(others[0]).is_none());
        // A dropped account loads again from the database.
        assert_eq!(state.learner(others[0]).await.unwrap().user, others[0]);
    }

    #[tokio::test]
    async fn cancelled_updates_finish_and_publish_in_order() {
        let dir = TempDir::new("progress-updates");
        let state = test_state(&dir.path(""), "tcp://127.0.0.1:1");
        let learner = test_learner(&state, "a@example.com").await;
        let (written, writing) = tokio::sync::oneshot::channel();
        let (resume, paused) = std::sync::mpsc::channel();
        let first_state = Arc::clone(&state);
        let first_learner = Arc::clone(&learner);
        let first = tokio::spawn(async move {
            first_state
                .update_progress(&first_learner, move |state, learner| {
                    state.store.save_note(learner.user, "a", "first", 1)?;
                    written.send(()).unwrap();
                    paused.recv().unwrap();
                    learner
                        .progress
                        .write()
                        .notes
                        .insert("a".into(), "first".into());
                    Ok(())
                })
                .await
        });
        writing.await.unwrap();
        // Drop the HTTP task after the durable write, before publication.
        first.abort();
        assert!(first.await.unwrap_err().is_cancelled());
        let second_state = Arc::clone(&state);
        let second_learner = Arc::clone(&learner);
        let (entered, mut entering) = tokio::sync::oneshot::channel();
        let second = tokio::spawn(async move {
            second_state
                .update_progress(&second_learner, move |state, learner| {
                    entered.send(()).unwrap();
                    state.store.save_note(learner.user, "a", "second", 2)?;
                    learner
                        .progress
                        .write()
                        .notes
                        .insert("a".into(), "second".into());
                    Ok(())
                })
                .await
        });
        let entered_early =
            tokio::time::timeout(std::time::Duration::from_millis(30), &mut entering)
                .await
                .is_ok();
        resume.send(()).unwrap();
        second.await.unwrap().unwrap();
        assert!(
            !entered_early,
            "the later update overtook an unfinished write"
        );
        assert_eq!(
            learner.progress.read().notes,
            state.store.notes(learner.user).unwrap()
        );
        assert_eq!(learner.progress.read().notes["a"], "second");
    }

    #[tokio::test]
    async fn a_deleted_account_takes_no_more_writes() {
        let dir = TempDir::new("progress-deleted");
        let state = test_state(&dir.path(""), "tcp://127.0.0.1:1");
        let learner = test_learner(&state, "a@example.com").await;
        state.delete_account(&learner).await.unwrap();
        let late = state
            .update_progress(&learner, |state, learner| {
                state.store.save_note(learner.user, "a", "late", 1)
            })
            .await;
        assert!(matches!(late, Err(ApiError::SignIn)));
        assert!(state.store.notes(learner.user).unwrap().is_empty());
    }
}
