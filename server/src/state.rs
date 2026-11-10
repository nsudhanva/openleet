//! Shared server state: static content, the in-memory progress cache, storage and the judge.

use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use anyhow::Result;
use parking_lot::{Mutex, RwLock};

use openleet::content::Content;
use openleet::model::{Attempt, CompanyFilter, Problem};
use openleet::scheduler::{CardStates, card_states, record_attempt};
use openleet::scorer::{ScoreReport, day_key, score_report};
use openleet::service;

use crate::acme::CertificateSlot;
use crate::db::{DailyScore, Store};
use crate::error::{ApiError, ApiResult};
use crate::judge::Judge;

/// Everything derived from the attempt log, kept in memory so reads never touch the disk.
pub struct Progress {
    /// The attempt log, oldest first.
    pub attempts: Vec<Attempt>,
    /// Card state per slug, replayed from `attempts`.
    pub states: CardStates,
    /// Your answer per slug.
    pub notes: HashMap<String, String>,
    /// Slugs with an accepted submission.
    pub solved: HashSet<String>,
    /// Reports per company, computed on first read after the log changed.
    reports: HashMap<CompanyFilter, ScoreReport>,
}

impl Progress {
    /// Replays the attempt log into card states.
    pub fn new(
        attempts: Vec<Attempt>,
        notes: HashMap<String, String>,
        solved: HashSet<String>,
    ) -> Self {
        let states = card_states(&attempts);
        Self {
            attempts,
            states,
            notes,
            solved,
            reports: HashMap::new(),
        }
    }

    /// Records a new attempt.
    pub fn push(&mut self, attempt: Attempt) {
        record_attempt(&mut self.states, &attempt);
        self.attempts.push(attempt);
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

    /// Drops every cached report, so the next reads see memory decay up to now.
    pub fn invalidate_reports(&mut self) {
        self.reports.clear();
    }

    /// A company's report, computed only on the first read after the log changed.
    pub fn report(&mut self, content: &Content, company: CompanyFilter, now: i64) -> &ScoreReport {
        self.reports
            .entry(company)
            .or_insert_with(|| score_report(content, company, &self.attempts, &self.states, now))
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
    pub progress: RwLock<Progress>,
    /// Serializes durable progress writes with publication to the in-memory cache.
    pub progress_updates: Mutex<()>,
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
    /// The problem with this slug, or a 404.
    pub fn problem(&self, slug: &str) -> ApiResult<&Problem> {
        Ok(service::problem_of(&self.content, slug)?)
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

    /// Finishes a durable write and its cache update together, even if the HTTP request is
    /// cancelled. The cache lock is only held when publishing, so reads need not wait on IO.
    pub async fn update_progress<T: Send + 'static>(
        self: &Arc<Self>,
        work: impl FnOnce(&Self) -> Result<T> + Send + 'static,
    ) -> ApiResult<T> {
        let state = Arc::clone(self);
        tokio::task::spawn_blocking(move || {
            let _update = state.progress_updates.lock();
            work(&state)
        })
        .await
        .map_err(|e| ApiError::Internal(e.into()))?
        .map_err(ApiError::Internal)
    }

    /// Recomputes the default company's report and stores today's scores. Other companies'
    /// reports are recomputed when next read.
    pub async fn refresh_scores(self: &Arc<Self>) -> ApiResult<()> {
        self.update_progress(|state| state.save_scores()).await
    }

    fn save_scores(&self) -> Result<()> {
        let now = now_ms();
        let score = {
            let mut progress = self.progress.write();
            progress.invalidate_reports();
            let report = progress.report(&self.content, self.content.default_company(), now);
            (report.graded > 0).then(|| DailyScore {
                day: day_key(now),
                readiness: report.readiness,
                coverage: report.coverage,
                accuracy: report.accuracy,
            })
        };
        if let Some(score) = score {
            self.store.save_daily_score(now, &score)?;
        }
        Ok(())
    }
}

/// A state over empty content, a new database in `dir` and a judge at `judge`, for tests.
#[cfg(test)]
pub fn test_state(dir: &std::path::Path, judge: &str) -> Shared {
    let none = dir.join("none.json");
    test_state_with(dir, judge, Content::load(&none, &none).expect("content"))
}

/// [`test_state`] over the given content.
#[cfg(test)]
pub fn test_state_with(dir: &std::path::Path, judge: &str, content: Content) -> Shared {
    let none = dir.join("none.json");
    let (store, _) =
        Store::open(&dir.join("openleet.duckdb"), &dir.join("none.duckdb")).expect("database");
    let judge = Judge::load(&none, judge.parse().expect("endpoint"), 1.0).expect("judge");
    Arc::new(AppState {
        companies: crate::api::companies_response(&content),
        content,
        revision: "test".to_owned(),
        deploy: None,
        store,
        judge,
        progress: RwLock::new(Progress::new(Vec::new(), HashMap::new(), HashSet::new())),
        progress_updates: Mutex::new(()),
        certificate: CertificateSlot::default(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::db::testing::TempDir;

    #[tokio::test]
    async fn cancelled_updates_finish_and_publish_in_order() {
        let dir = TempDir::new("progress-updates");
        let state = test_state(&dir.path(""), "tcp://127.0.0.1:1");
        let (written, writing) = tokio::sync::oneshot::channel();
        let (resume, paused) = std::sync::mpsc::channel();
        let first_state = Arc::clone(&state);
        let first = tokio::spawn(async move {
            first_state
                .update_progress(move |state| {
                    state.store.save_note("a", "first", 1)?;
                    written.send(()).unwrap();
                    paused.recv().unwrap();
                    state
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
        let (entered, mut entering) = tokio::sync::oneshot::channel();
        let second = tokio::spawn(async move {
            second_state
                .update_progress(move |state| {
                    entered.send(()).unwrap();
                    state.store.save_note("a", "second", 2)?;
                    state
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
        assert_eq!(state.progress.read().notes, state.store.notes().unwrap());
        assert_eq!(state.progress.read().notes["a"], "second");
    }
}
