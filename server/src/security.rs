//! Hardening shared by every response: security headers, request timeouts and a global limit
//! on requests in flight.

use std::sync::LazyLock;
use std::time::Duration;

use axum::http::{HeaderValue, StatusCode, header};
use axum::response::Response;
use tower_http::timeout::TimeoutLayer;

/// The inline scripts of the embedded index.html (the theme script), hashed by build.rs.
static SCRIPT_HASHES: &[&str] = include!(concat!(env!("OUT_DIR"), "/script_hashes.rs"));

/// Requests handled at once; more wait for a turn.
pub const MAX_IN_FLIGHT: usize = 256;
/// How long a request may take, except running code.
pub const REQUEST_TIMEOUT: Duration = Duration::from_secs(15);
/// How long Run and Submit may take: queueing behind other jobs, then the judge's own limit.
pub const JUDGE_TIMEOUT: Duration = Duration::from_secs(120);
/// How long a client may take to send a request's headers (HTTPS listeners).
pub const HEADER_READ_TIMEOUT: Duration = Duration::from_secs(10);

/// The policy for the web app: its own scripts and the hashed inline ones, inline styles
/// (the editor sets them), statement images from jsDelivr, and nothing else.
fn content_security_policy(script_hashes: &[&str]) -> String {
    let scripts = std::iter::once("'self'")
        .chain(script_hashes.iter().copied())
        .collect::<Vec<_>>()
        .join(" ");
    format!(
        "default-src 'self'; script-src {scripts}; style-src 'self' 'unsafe-inline'; \
         img-src 'self' https://fastly.jsdelivr.net data:; connect-src 'self'; \
         object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
    )
}

static CSP: LazyLock<HeaderValue> = LazyLock::new(|| {
    HeaderValue::from_str(&content_security_policy(SCRIPT_HASHES)).expect("the policy is ASCII")
});

/// Adds the security headers to a response.
pub async fn headers(mut response: Response) -> Response {
    let headers = response.headers_mut();
    headers.insert(header::CONTENT_SECURITY_POLICY, CSP.clone());
    headers.insert(
        header::X_CONTENT_TYPE_OPTIONS,
        HeaderValue::from_static("nosniff"),
    );
    headers.insert(
        header::REFERRER_POLICY,
        HeaderValue::from_static("strict-origin-when-cross-origin"),
    );
    headers.insert(header::X_FRAME_OPTIONS, HeaderValue::from_static("DENY"));
    response
}

/// Ends a request that takes longer than `limit` with a 503.
pub fn timeout(limit: Duration) -> TimeoutLayer {
    TimeoutLayer::with_status_code(StatusCode::SERVICE_UNAVAILABLE, limit)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_policy_allows_the_hashed_inline_scripts_only() {
        let policy = content_security_policy(&["'sha256-abc='"]);
        assert!(
            policy.contains("script-src 'self' 'sha256-abc=';"),
            "{policy}"
        );
        assert!(policy.starts_with("default-src 'self';"));
        assert!(policy.contains("frame-ancestors 'none'"));
        assert!(content_security_policy(&[]).contains("script-src 'self';"));
    }

    #[tokio::test]
    async fn every_response_gets_the_headers() {
        let response = headers(Response::default()).await;
        for name in [
            header::CONTENT_SECURITY_POLICY,
            header::X_CONTENT_TYPE_OPTIONS,
            header::REFERRER_POLICY,
            header::X_FRAME_OPTIONS,
        ] {
            assert!(response.headers().contains_key(&name), "{name}");
        }
    }
}
