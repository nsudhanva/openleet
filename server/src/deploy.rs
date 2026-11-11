//! Push-to-deploy: CI asks for a release with a signed webhook, and the server only records
//! the request. A systemd path unit watches the file and runs the updater as root; the server
//! itself never runs anything.

use std::path::{Path, PathBuf};

use axum::body::Bytes;
use axum::extract::State;
use axum::http::{HeaderMap, StatusCode};
use hmac::{Hmac, KeyInit, Mac};
use serde::Deserialize;
use sha2::Sha256;

use crate::error::{ApiError, ApiResult};
use crate::state::Shared;

/// Largest webhook body accepted.
pub const MAX_BODY: usize = 1024;
/// The request header with the body's signature, `sha256=<hex HMAC-SHA256>`.
const SIGNATURE_HEADER: &str = "x-deploy-signature";
/// The file the systemd path unit watches, in `STATE_DIR`.
const REQUEST_FILE: &str = "deploy-request";

/// The webhook's settings; present only when `DEPLOY_SECRET` is set.
pub struct Deploy {
    secret: Box<[u8]>,
    request: PathBuf,
    writer: std::sync::Arc<parking_lot::Mutex<()>>,
}

impl Deploy {
    /// Enabled by a non-empty `secret`; requests are written to `state_dir/deploy-request`.
    #[must_use]
    pub fn new(secret: Option<String>, state_dir: &Path) -> Option<Self> {
        secret.filter(|s| !s.is_empty()).map(|secret| Self {
            secret: secret.into_bytes().into_boxed_slice(),
            request: state_dir.join(REQUEST_FILE),
            writer: std::sync::Arc::new(parking_lot::Mutex::new(())),
        })
    }

    async fn record(&self, revision: &str) -> std::io::Result<()> {
        let writer = std::sync::Arc::clone(&self.writer);
        let request = self.request.clone();
        let contents = format!("{revision}\n");
        // A cancelled HTTP request must not release the lock while its filesystem work is
        // still running; both the write and rename finish in this one blocking task.
        tokio::task::spawn_blocking(move || {
            let _writer = writer.lock();
            write_atomically(&request, &contents)
        })
        .await
        .map_err(std::io::Error::other)?
    }
}

const fn hex_digit(byte: u8) -> Option<u8> {
    match byte {
        b'0'..=b'9' => Some(byte - b'0'),
        b'a'..=b'f' => Some(byte - b'a' + 10),
        b'A'..=b'F' => Some(byte - b'A' + 10),
        _ => None,
    }
}

fn decode_hex(text: &str) -> Option<Vec<u8>> {
    let (pairs, rest) = text.as_bytes().as_chunks::<2>();
    if !rest.is_empty() {
        return None;
    }
    pairs
        .iter()
        .map(|&[high, low]| Some(hex_digit(high)? << 4 | hex_digit(low)?))
        .collect()
}

/// Whether `header` (`sha256=<hex>`) is the HMAC-SHA256 of `body` under `secret`. The MAC is
/// compared in constant time.
#[must_use]
pub fn verify(secret: &[u8], body: &[u8], header: &str) -> bool {
    let Some(signature) = header.trim().strip_prefix("sha256=").and_then(decode_hex) else {
        return false;
    };
    let Ok(mut mac) = Hmac::<Sha256>::new_from_slice(secret) else {
        return false;
    };
    mac.update(body);
    mac.verify_slice(&signature).is_ok()
}

#[derive(Deserialize)]
struct DeployRequest {
    revision: String,
}

/// A short or full git revision: 7 to 40 lowercase hex digits.
fn valid_revision(revision: &str) -> bool {
    (7..=40).contains(&revision.len())
        && revision
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

/// Writes `contents` to `path` through a temporary file and a rename, so the watcher never
/// reads a half-written file.
fn write_atomically(path: &Path, contents: &str) -> std::io::Result<()> {
    let temporary = path.with_extension("tmp");
    std::fs::write(&temporary, contents)?;
    std::fs::rename(&temporary, path)
}

/// `POST /api/deploy`: 202 once the request is recorded, 401 for a bad signature, 404 when
/// deploys are off. The route caps the body at [`MAX_BODY`] (413).
pub async fn deploy(
    State(state): State<Shared>,
    headers: HeaderMap,
    body: Bytes,
) -> ApiResult<StatusCode> {
    let Some(deploy) = &state.deploy else {
        return Err(ApiError::no_endpoint());
    };
    let signature = headers
        .get(SIGNATURE_HEADER)
        .and_then(|v| v.to_str().ok())
        .unwrap_or_default();
    if !verify(&deploy.secret, &body, signature) {
        return Err(ApiError::Unauthorized);
    }
    let request: DeployRequest = serde_json::from_slice(&body)
        .map_err(|e| ApiError::BadRequest(format!("Invalid deploy request: {e}")))?;
    if !valid_revision(&request.revision) {
        return Err(ApiError::BadRequest("revision must be a git hash".into()));
    }
    deploy
        .record(&request.revision)
        .await
        .map_err(|e| ApiError::Internal(e.into()))?;
    tracing::info!("deploy of {} requested", request.revision);
    Ok(StatusCode::ACCEPTED)
}

/// The running release: the `REVISION` file next to the data directory, trimmed, or "dev".
#[must_use]
pub fn revision(data_dir: &Path) -> String {
    std::fs::read_to_string(data_dir.join("..").join("REVISION"))
        .ok()
        .map(|text| text.trim().to_owned())
        .filter(|text| !text.is_empty())
        .unwrap_or_else(|| "dev".to_owned())
}

#[cfg(test)]
mod tests {
    use std::fmt::Write as _;

    use super::*;

    fn sign(secret: &[u8], body: &[u8]) -> String {
        let mut mac = Hmac::<Sha256>::new_from_slice(secret).expect("any key length");
        mac.update(body);
        let bytes = mac.finalize().into_bytes();
        bytes.iter().fold("sha256=".to_owned(), |mut text, b| {
            let _ = write!(text, "{b:02x}");
            text
        })
    }

    #[test]
    fn accepts_only_the_right_signature() {
        let body = br#"{"revision":"0123456789ab"}"#;
        let good = sign(b"secret", body);
        assert!(verify(b"secret", body, &good));
        assert!(verify(
            b"secret",
            body,
            &good.to_uppercase().replace("SHA256=", "sha256=")
        ));
        assert!(!verify(b"other", body, &good));
        assert!(!verify(b"secret", br#"{"revision":"0123456789ac"}"#, &good));
        assert!(!verify(b"secret", body, good.trim_start_matches("sha256=")));
        assert!(!verify(b"secret", body, &good[..good.len() - 2]));
        assert!(!verify(b"secret", body, "sha256=zz"));
        assert!(!verify(b"secret", body, ""));
    }

    #[test]
    fn checks_revisions() {
        assert!(valid_revision("0123456789ab"));
        assert!(!valid_revision("0123456789AB"));
        assert!(!valid_revision("../../etc"));
        assert!(!valid_revision("abc"));
    }

    #[test]
    fn is_off_without_a_secret() {
        assert!(Deploy::new(None, Path::new("/state")).is_none());
        assert!(Deploy::new(Some(String::new()), Path::new("/state")).is_none());
        let on = Deploy::new(Some("s".into()), Path::new("/state")).expect("on");
        assert_eq!(on.request, Path::new("/state/deploy-request"));
    }

    #[tokio::test]
    async fn writes_requests_atomically() {
        let dir = std::env::temp_dir().join(format!("openleet-deploy-{}", std::process::id()));
        std::fs::create_dir_all(dir.join("data")).expect("temp dir");
        let path = dir.join(REQUEST_FILE);
        write_atomically(&path, "0123456789ab\n").expect("write");
        assert_eq!(
            std::fs::read_to_string(&path).expect("read"),
            "0123456789ab\n"
        );
        assert!(!path.with_extension("tmp").exists());
        assert_eq!(revision(&dir.join("data")), "dev");
        std::fs::write(dir.join("REVISION"), "abc123\n").expect("write");
        assert_eq!(revision(&dir.join("data")), "abc123");
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[tokio::test]
    async fn concurrent_requests_write_complete_revisions() {
        let dir = crate::db::testing::TempDir::new("deploy-concurrent");
        let deploy = std::sync::Arc::new(Deploy::new(Some("s".into()), &dir.path("")).unwrap());
        let mut requests = tokio::task::JoinSet::new();
        for revision in 0..32 {
            let deploy = std::sync::Arc::clone(&deploy);
            requests.spawn(async move { deploy.record(&format!("{revision:040x}")).await });
        }
        while let Some(request) = requests.join_next().await {
            request.unwrap().unwrap();
        }
        let contents = std::fs::read_to_string(&deploy.request).unwrap();
        assert_eq!(contents.len(), 41);
        assert!(valid_revision(contents.trim()));
        assert!(!deploy.request.with_extension("tmp").exists());
    }
}
