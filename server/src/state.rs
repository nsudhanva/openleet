//! Shared server state: static content, the in-memory progress cache, storage and the judge.

use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use anyhow::Result;
use parking_lot::RwLock;

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

    /// Recomputes the default company's report and stores today's scores. Other companies'
    /// reports are recomputed when next read.
    pub async fn refresh_scores(self: &Arc<Self>) -> ApiResult<()> {
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
            self.db(move |store| store.save_daily_score(now, &score))
                .await?;
        }
        Ok(())
    }
}

/// A state over empty content, a new database in `dir` and a judge at `judge`, for tests.
#[cfg(test)]
pub fn test_state(dir: &std::path::Path, judge: &str) -> Shared {
    let none = dir.join("none.json");
    let content = Content::load(&none, &none).expect("content");
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
        certificate: CertificateSlot::default(),
    })
}
