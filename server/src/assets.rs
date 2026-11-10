//! Serves the web app embedded by build.rs: precompressed files, strong ETags, year-long
//! caching for hashed assets, and index.html for every other path (client-side routing), with
//! preloads for the data that page loads first (src/preload.rs).

use std::collections::HashMap;
use std::sync::LazyLock;

use axum::body::Body;
use axum::http::{HeaderMap, HeaderValue, StatusCode, Uri, header};
use axum::response::{IntoResponse, Response};

use crate::{fingerprint, preload};

/// One embedded file with its precompressed variants.
pub struct Asset {
    pub path: &'static str,
    pub mime: &'static str,
    pub etag: &'static str,
    pub raw: &'static [u8],
    pub br: Option<&'static [u8]>,
    pub zstd: Option<&'static [u8]>,
}

/// index.html cut where a page's preloads go (before `</body>`), with the part before also
/// compressed and left open (flushed, not finished), so a response only appends the rest.
pub struct Page {
    pub head: &'static [u8],
    pub tail: &'static [u8],
    pub br_head: &'static [u8],
    pub zstd_head: &'static [u8],
}

static ASSETS: &[Asset] = include!(concat!(env!("OUT_DIR"), "/assets.rs"));
static PAGE: Option<Page> = include!(concat!(env!("OUT_DIR"), "/page.rs"));
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
    if asset.path == INDEX
        && let Some(page) = &PAGE
    {
        return serve_page(page, asset, &uri, &headers);
    }
    let cache = if asset.path.starts_with("/assets/") {
        IMMUTABLE
    } else {
        REVALIDATE
    };
    respond(
        &headers,
        asset.mime,
        cache,
        asset.etag,
        |coding| match coding {
            Coding::Br => asset.br.map(Body::from),
            Coding::Zstd => asset.zstd.map(Body::from),
            Coding::Identity => Some(Body::from(asset.raw)),
        },
    )
}

/// index.html with `<link rel="preload">` tags for the data the page at `uri` loads first.
fn serve_page(page: &Page, asset: &Asset, uri: &Uri, headers: &HeaderMap) -> Response {
    let links = preload::links(uri.path(), uri.query());
    let etag = fingerprint::etag(&[asset.etag.as_bytes(), links.as_bytes()].concat());
    let rest = [links.as_bytes(), page.tail].concat();
    respond(headers, asset.mime, REVALIDATE, &etag, |coding| {
        Some(Body::from(match coding {
            Coding::Br => brotli_append(page.br_head, &rest),
            Coding::Zstd => zstd_append(page.zstd_head, &rest),
            Coding::Identity => [page.head, &rest].concat(),
        }))
    })
}

#[derive(Clone, Copy)]
enum Coding {
    Br,
    Zstd,
    Identity,
}

/// A 200 with the body in the best coding the client accepts and `body` offers, or a 304.
fn respond(
    headers: &HeaderMap,
    mime: &'static str,
    cache: &'static str,
    etag: &str,
    body: impl Fn(Coding) -> Option<Body>,
) -> Response {
    let response = Response::builder()
        .header(header::CONTENT_TYPE, mime)
        .header(header::CACHE_CONTROL, cache)
        .header(header::ETAG, etag)
        .header(header::VARY, "accept-encoding");
    if headers
        .get(header::IF_NONE_MATCH)
        .is_some_and(|v| v.as_bytes() == etag.as_bytes())
    {
        return response
            .status(StatusCode::NOT_MODIFIED)
            .body(Body::empty())
            .unwrap_or_default();
    }
    let encoded = [(Coding::Br, "br"), (Coding::Zstd, "zstd")]
        .into_iter()
        .filter(|(_, name)| accepts(headers, name))
        .find_map(|(coding, name)| Some((body(coding)?, name)));
    match encoded {
        Some((body, name)) => response
            .header(header::CONTENT_ENCODING, HeaderValue::from_static(name))
            .body(body),
        None => response.body(body(Coding::Identity).unwrap_or_default()),
    }
    .unwrap_or_default()
}

/// Ends a Brotli stream that was flushed (so it ends on a byte boundary) but not finished with
/// `rest` stored as is: uncompressed meta-blocks of at most 64 KiB, then an empty last one
/// (RFC 7932, section 9.2).
fn brotli_append(head: &[u8], rest: &[u8]) -> Vec<u8> {
    const MAX_BLOCK: usize = 1 << 16;
    let mut out = Vec::with_capacity(head.len() + rest.len() + 4 * rest.len().div_ceil(MAX_BLOCK));
    out.extend_from_slice(head);
    for block in rest.chunks(MAX_BLOCK) {
        // ISLAST 0, MNIBBLES 00 (four), MLEN - 1 in 16 bits, ISUNCOMPRESSED 1, zero padding.
        let mlen = u32::try_from(block.len() - 1).unwrap_or_default();
        out.extend_from_slice(&((mlen << 3) | (1 << 19)).to_le_bytes()[..3]);
        out.extend_from_slice(block);
    }
    out.push(0b11); // ISLAST, ISLASTEMPTY
    out
}

/// Ends a zstd frame that was flushed but not finished (no content size, no checksum) with
/// `rest` as raw blocks of at most 128 KiB, the last one marked (RFC 8878, section 3.1.1.2).
fn zstd_append(head: &[u8], rest: &[u8]) -> Vec<u8> {
    const MAX_BLOCK: usize = 128 << 10;
    let mut out = Vec::with_capacity(head.len() + rest.len() + 3 * rest.len().div_ceil(MAX_BLOCK));
    out.extend_from_slice(head);
    let blocks = rest.len().div_ceil(MAX_BLOCK);
    for (i, block) in rest.chunks(MAX_BLOCK).enumerate() {
        // Last_Block, Block_Type 0 (raw), Block_Size.
        let size = u32::try_from(block.len()).unwrap_or_default();
        let last = u32::from(i + 1 == blocks);
        out.extend_from_slice(&((size << 3) | last).to_le_bytes()[..3]);
        out.extend_from_slice(block);
    }
    out
}

#[cfg(test)]
mod tests {
    use std::io::Read as _;

    use axum::body::to_bytes;

    use super::*;

    async fn get(path: &str, encoding: &str) -> Response {
        let mut headers = HeaderMap::new();
        headers.insert(
            header::ACCEPT_ENCODING,
            HeaderValue::from_str(encoding).unwrap(),
        );
        serve(path.parse().unwrap(), headers).await
    }

    async fn body(response: Response) -> Vec<u8> {
        to_bytes(response.into_body(), usize::MAX)
            .await
            .unwrap()
            .to_vec()
    }

    #[test]
    fn appended_streams_decode() {
        let head = b"<!doctype html><p>".repeat(500);
        let rest = b"<link rel=preload></body>\n</html>\n".repeat(3000); // two blocks each
        let expected = [&head[..], &rest[..]].concat();

        let mut brotli = brotli::CompressorWriter::new(Vec::new(), 4096, 11, 22);
        std::io::Write::write_all(&mut brotli, &head).unwrap();
        std::io::Write::flush(&mut brotli).unwrap();
        let stream = brotli_append(brotli.get_ref(), &rest);
        let mut decoded = Vec::new();
        brotli::Decompressor::new(&stream[..], 4096)
            .read_to_end(&mut decoded)
            .unwrap();
        assert_eq!(decoded, expected);

        let mut zstd = zstd::stream::write::Encoder::new(Vec::new(), 19).unwrap();
        zstd.include_contentsize(false).unwrap();
        zstd.include_checksum(false).unwrap();
        std::io::Write::write_all(&mut zstd, &head).unwrap();
        std::io::Write::flush(&mut zstd).unwrap();
        let stream = zstd_append(zstd.get_ref(), &rest);
        assert_eq!(zstd::decode_all(&stream[..]).unwrap(), expected);
    }

    #[tokio::test]
    async fn pages_carry_their_preloads_in_every_coding() {
        let Some(page) = &PAGE else {
            return; // an API-only build embeds no web app
        };
        let plain = body(get("/code/two-sum?x=1", "identity").await).await;
        let links = preload::links("/code/two-sum", Some("x=1"));
        assert_eq!(plain, [page.head, links.as_bytes(), page.tail].concat());
        assert!(links.contains("/api/code/two-sum"));

        let response = get("/code/two-sum?x=1", "gzip, br").await;
        assert_eq!(response.headers()[header::CONTENT_ENCODING], "br");
        let mut decoded = Vec::new();
        brotli::Decompressor::new(&body(response).await[..], 4096)
            .read_to_end(&mut decoded)
            .unwrap();
        assert_eq!(decoded, plain);

        let response = get("/code/two-sum?x=1", "zstd").await;
        assert_eq!(response.headers()[header::CONTENT_ENCODING], "zstd");
        assert_eq!(zstd::decode_all(&body(response).await[..]).unwrap(), plain);
    }

    #[tokio::test]
    async fn each_page_has_its_own_etag() {
        if PAGE.is_none() {
            return;
        }
        let etag = |response: &Response| response.headers()[header::ETAG].clone();
        let home = get("/", "br").await;
        let problems = get("/problems", "br").await;
        assert_ne!(etag(&home), etag(&problems));
        let mut headers = HeaderMap::new();
        headers.insert(header::IF_NONE_MATCH, etag(&problems));
        let again = serve("/problems".parse().unwrap(), headers).await;
        assert_eq!(again.status(), StatusCode::NOT_MODIFIED);
    }
}
