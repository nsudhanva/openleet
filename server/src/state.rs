//! Shared server state: static content, the in-memory progress cache, storage and the judge.

use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use anyhow::Result;
use parking_lot::RwLock;

use cards::content::Content;
use cards::model::Attempt;
use cards::scheduler::{CardStates, card_states, record_attempt};
use cards::scorer::{ScoreReport, day_key, score_report_with};

use crate::db::{DailyScore, Store};
use crate::error::{ApiError, ApiResult};
use crate::judge::Judge;

/// Everything derived from the attempt log, kept in memory so reads never touch the disk.
pub struct Progress {
    pub attempts: Vec<Attempt>,
    pub states: CardStates,
    pub notes: HashMap<String, String>,
    pub solved: HashSet<String>,
    report: Option<ScoreReport>,
}

impl Progress {
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
            report: None,
        }
    }

    pub fn push(&mut self, attempt: Attempt) {
        record_attempt(&mut self.states, &attempt);
        self.attempts.push(attempt);
        self.report = None;
    }

    pub fn clear(&mut self, slug: Option<&str>) {
        match slug {
            Some(slug) => self.attempts.retain(|a| a.slug != slug),
            None => self.attempts.clear(),
        }
        self.states = card_states(&self.attempts);
        self.report = None;
    }

    /// The current report, recomputed only after the log changed (or when asked to).
    pub fn report(&mut self, content: &Content, now: i64, fresh: bool) -> &ScoreReport {
        let report = match self.report.take() {
            Some(report) if !fresh => report,
            _ => score_report_with(&content.problems, &self.attempts, &self.states, now),
        };
        self.report.insert(report)
    }
}

pub struct AppState {
    pub content: Content,
    pub store: Store,
    pub judge: Judge,
    pub progress: RwLock<Progress>,
}

pub type Shared = Arc<AppState>;

pub fn now_ms() -> i64 {
    jiff::Timestamp::now().as_millisecond()
}

impl AppState {
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

    /// Recomputes the report and stores today's scores, like the old background scorer.
    pub async fn refresh_scores(self: &Arc<Self>) -> ApiResult<()> {
        let now = now_ms();
        let score = {
            let mut progress = self.progress.write();
            let report = progress.report(&self.content, now, true);
            (report.graded > 0).then(|| DailyScore {
                day: day_key(now),
                readiness: report.readiness,
                coverage: report.coverage,
                accuracy: report.accuracy,
            })
        };
        if let Some(score) = score {
            self.db(move |store| store.save_daily_score(&score.day, now, &score))
                .await?;
        }
        Ok(())
    }
}
