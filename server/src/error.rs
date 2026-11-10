//! API errors: every failure becomes `{"error": "..."}` with a fitting status.

use axum::Json;
use axum::http::StatusCode;
use axum::response::{IntoResponse, Response};
use serde_json::json;

use openleet::service::{InvalidInput, UnknownProblem};

/// Why a request failed; each variant maps to one HTTP status.
#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    #[error("{0}")]
    BadRequest(String),
    #[error("{0}")]
    NotFound(String),
    #[error("Bad signature")]
    Unauthorized,
    #[error("The judge is busy; try again in a few seconds.")]
    Busy,
    #[error("The judge is not available.")]
    JudgeDown,
    #[error(transparent)]
    Internal(#[from] anyhow::Error),
}

pub type ApiResult<T> = Result<T, ApiError>;

impl ApiError {
    /// The 404 for a path no endpoint serves (or a disabled one).
    pub fn no_endpoint() -> Self {
        Self::NotFound("No such endpoint".into())
    }
}

impl From<UnknownProblem> for ApiError {
    fn from(error: UnknownProblem) -> Self {
        Self::NotFound(error.to_string())
    }
}

impl From<InvalidInput> for ApiError {
    fn from(error: InvalidInput) -> Self {
        Self::BadRequest(error.to_string())
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let status = match &self {
            Self::BadRequest(_) => StatusCode::BAD_REQUEST,
            Self::NotFound(_) => StatusCode::NOT_FOUND,
            Self::Unauthorized => StatusCode::UNAUTHORIZED,
            Self::Busy | Self::JudgeDown => StatusCode::SERVICE_UNAVAILABLE,
            Self::Internal(error) => {
                tracing::error!("{error:#}");
                StatusCode::INTERNAL_SERVER_ERROR
            }
        };
        let message = match &self {
            Self::Internal(_) => "Internal error".to_owned(),
            other => other.to_string(),
        };
        (status, Json(json!({ "error": message }))).into_response()
    }
}
