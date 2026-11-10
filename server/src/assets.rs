//! Serves the web app embedded by build.rs: precompressed files, strong ETags, year-long
//! caching for hashed assets, and index.html for every other path (client-side routing).

use std::collections::HashMap;
use std::sync::LazyLock;

use axum::body::Body;
use axum::http::{HeaderMap, HeaderValue, StatusCode, Uri, header};
use axum::response::{IntoResponse, Response};

/// One embedded file with its precompressed variants.
pub struct Asset {
    pub path: &'static str,
    pub mime: &'static str,
    pub etag: &'static str,
    pub raw: &'static [u8],
    pub br: Option<&'static [u8]>,
    pub zstd: Option<&'static [u8]>,
}

static ASSETS: &[Asset] = include!(concat!(env!("OUT_DIR"), "/assets.rs"));
static BY_PATH: LazyLock<HashMap<&'static str, &'static Asset>> =
    LazyLock::new(|| ASSETS.iter().map(|a| (a.path, a)).collect());

const INDEX: &str = "/index.html";
const IMMUTABLE: &str = "public, max-age=31536000, immutable";
const REVALIDATE: &str = "no-cache";

/// Whether the build embedded a web app at all (it is optional for API-only builds).
pub fn embedded() -> usize {
    ASSETS.len()
}

fn accepts(headers: &HeaderMap, coding: &str) -> bool {
    headers
        .get_all(header::ACCEPT_ENCODING)
        .iter()
        .filter_map(|v| v.to_str().ok())
        .flat_map(|v| v.split(','))
        .any(|part| {
            let mut pieces = part.trim().split(';');
            pieces.next() == Some(coding) && !pieces.any(|p| p.trim() == "q=0")
        })
}

/// Serves an embedded file, or the app's index.html for client-side routes.
pub async fn serve(uri: Uri, headers: HeaderMap) -> Response {
    let path = uri.path();
    let asset = BY_PATH.get(path).or_else(|| {
        // Paths that look like files must exist; everything else is a page of the app.
        let last = path.rsplit('/').next().unwrap_or_default();
        (!last.contains('.')).then(|| BY_PATH.get(INDEX)).flatten()
    });
    let Some(asset) = asset else {
        return StatusCode::NOT_FOUND.into_response();
    };
    let cache = if asset.path.starts_with("/assets/") {
        IMMUTABLE
    } else {
        REVALIDATE
    };
    let mut response = Response::builder()
        .header(header::CONTENT_TYPE, asset.mime)
        .header(header::CACHE_CONTROL, cache)
        .header(header::ETAG, asset.etag)
        .header(header::VARY, "accept-encoding");
    if headers
        .get(header::IF_NONE_MATCH)
        .is_some_and(|v| v.as_bytes() == asset.etag.as_bytes())
    {
        return response
            .status(StatusCode::NOT_MODIFIED)
            .body(Body::empty())
            .unwrap_or_default();
    }
    let (body, coding) = match (asset.br, asset.zstd) {
        (Some(br), _) if accepts(&headers, "br") => (br, Some("br")),
        (_, Some(zstd)) if accepts(&headers, "zstd") => (zstd, Some("zstd")),
        _ => (asset.raw, None),
    };
    if let Some(coding) = coding {
        response = response.header(header::CONTENT_ENCODING, HeaderValue::from_static(coding));
    }
    response.body(Body::from(body)).unwrap_or_default()
}
