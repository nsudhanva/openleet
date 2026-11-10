//! API errors: every failure becomes `{"error": "..."}` with a fitting status.

use axum::Json;
use axum::body::to_bytes;
use axum::http::{StatusCode, header};
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
        error_response(status, &message)
    }
}

fn error_response(status: StatusCode, message: &str) -> Response {
    (status, Json(json!({ "error": message }))).into_response()
}

/// Longest plain-text error body turned into a message; axum's rejections are one line.
const MAX_REJECTION_BYTES: usize = 4096;

/// The one place every other failure gets the API's error shape: axum's extractor rejections
/// (malformed JSON, a wrong content type, a bad path or query), an unknown method and the
/// timeout answer plain text or nothing. Their text becomes `{"error": "..."}`; a body that
/// is valid JSON but the wrong shape (422) is a 400 like any other invalid input.
pub async fn json_errors(response: Response) -> Response {
    let status = response.status();
    let is_json = response
        .headers()
        .get(header::CONTENT_TYPE)
        .is_some_and(|v| v.as_bytes().starts_with(b"application/json"));
    if !(status.is_client_error() || status.is_server_error()) || is_json {
        return response;
    }
    let status = if status == StatusCode::UNPROCESSABLE_ENTITY {
        StatusCode::BAD_REQUEST
    } else {
        status
    };
    let (parts, body) = response.into_parts();
    let text = to_bytes(body, MAX_REJECTION_BYTES)
        .await
        .unwrap_or_default();
    let text = String::from_utf8_lossy(&text);
    let message = match text.trim() {
        "" => status.canonical_reason().unwrap_or("Request failed"),
        text => text,
    };
    let mut mapped = error_response(status, message);
    // Keep what the status needs, such as the methods a 405 allows.
    if let Some(allow) = parts.headers.get(header::ALLOW) {
        mapped.headers_mut().insert(header::ALLOW, allow.clone());
    }
    mapped
}

#[cfg(test)]
mod tests {
    use axum::Router;
    use axum::body::Body;
    use axum::http::{Method, Request};
    use axum::routing::post;
    use serde::Deserialize;
    use tower::ServiceExt as _;

    use super::*;

    #[derive(Deserialize)]
    struct Input {
        #[expect(dead_code, reason = "only parsed")]
        slug: String,
    }

    async fn call(
        method: Method,
        uri: &str,
        content_type: &str,
        body: &str,
    ) -> (StatusCode, serde_json::Value) {
        let app = Router::new()
            .route(
                "/items",
                post(|Json(_): Json<Input>| async { StatusCode::NO_CONTENT }),
            )
            .route(
                "/items/{id}",
                post(|axum::extract::Path(_): axum::extract::Path<i64>| async {
                    StatusCode::NO_CONTENT
                }),
            )
            .layer(axum::middleware::map_response(json_errors));
        let request = Request::builder()
            .method(method)
            .uri(uri)
            .header(header::CONTENT_TYPE, content_type)
            .body(Body::from(body.to_owned()))
            .expect("request");
        let response = app.oneshot(request).await.expect("response");
        let status = response.status();
        assert_eq!(
            response.headers()[header::CONTENT_TYPE],
            "application/json",
            "{status}"
        );
        let body = to_bytes(response.into_body(), 1 << 16).await.expect("body");
        (status, serde_json::from_slice(&body).expect("json"))
    }

    #[tokio::test]
    async fn rejections_become_json_errors() {
        let json = "application/json";
        let (status, body) = call(Method::POST, "/items", json, "{").await;
        assert_eq!(status, StatusCode::BAD_REQUEST);
        assert!(body["error"].as_str().unwrap().contains("JSON"), "{body}");
        // Valid JSON of the wrong shape is invalid input too.
        let (status, _) = call(Method::POST, "/items", json, r#"{"id": 1}"#).await;
        assert_eq!(status, StatusCode::BAD_REQUEST);
        // Only JSON bodies are read: a form or text/plain post stays a 415.
        let (status, body) = call(Method::POST, "/items", "text/plain", "{}").await;
        assert_eq!(status, StatusCode::UNSUPPORTED_MEDIA_TYPE);
        assert!(
            body["error"].as_str().unwrap().contains("Content-Type"),
            "{body}"
        );
        let (status, _) = call(Method::POST, "/items/abc", json, "").await;
        assert_eq!(status, StatusCode::BAD_REQUEST);
        let (status, body) = call(Method::GET, "/items", json, "").await;
        assert_eq!(status, StatusCode::METHOD_NOT_ALLOWED);
        assert_eq!(body["error"], "Method Not Allowed");
    }
}
