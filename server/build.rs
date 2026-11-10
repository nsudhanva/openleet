//! Embeds the built web app (web/dist) in the binary, compressed ahead of time with Brotli
//! (quality 11) and zstd (level 19), so serving a file costs no CPU at all, and hashes the
//! inline scripts of its index.html for the Content-Security-Policy (src/security.rs).
//!
//! index.html is also cut where each page's preloads go (src/assets.rs): for each route, the
//! part before, with preloads for that route's code (from Vite's manifest,
//! .vite/manifest.json, not embedded), is compressed here too, as a stream left open for the
//! page to finish.

#[path = "src/csp.rs"]
mod csp;
#[path = "src/fingerprint.rs"]
mod fingerprint;

use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Write as _;
use std::io::Write as _;
use std::path::{Path, PathBuf};
use std::{env, fs};

const COMPRESSIBLE: &[&str] = &[
    "html",
    "js",
    "css",
    "svg",
    "json",
    "txt",
    "webmanifest",
    "map",
];
/// Below this, compression headers cost more than they save.
const MIN_COMPRESS_BYTES: usize = 512;
/// Where src/assets.rs adds a page's preloads to index.html: at the end of the body, so all
/// of the page before it is the same for every page.
const PRELOADS_AT: &[u8] = b"</body>";

fn files(dir: &Path, out: &mut Vec<PathBuf>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            files(&path, out);
        } else {
            out.push(path);
        }
    }
}

fn mime(path: &Path) -> &'static str {
    match path
        .extension()
        .and_then(|e| e.to_str())
        .unwrap_or_default()
    {
        "html" => "text/html; charset=utf-8",
        "js" => "text/javascript; charset=utf-8",
        "css" => "text/css; charset=utf-8",
        "svg" => "image/svg+xml",
        "json" | "map" => "application/json",
        "webmanifest" => "application/manifest+json",
        "txt" => "text/plain; charset=utf-8",
        "woff2" => "font/woff2",
        "woff" => "font/woff",
        "png" => "image/png",
        "ico" => "image/x-icon",
        "webp" => "image/webp",
        _ => "application/octet-stream",
    }
}

fn main() {
    let dist = PathBuf::from(env::var("WEB_DIST").unwrap_or_else(|_| "../web/dist".into()));
    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR"));
    println!("cargo::rerun-if-env-changed=WEB_DIST");
    println!("cargo::rerun-if-changed={}", dist.display());

    let mut paths = Vec::new();
    files(&dist, &mut paths);
    // Vite's manifest is for this build only (route_chunks below), not for browsers.
    paths.retain(|p| !p.starts_with(dist.join(".vite")));
    paths.sort();
    let mut code = String::from("&[\n");
    for (i, path) in paths.iter().enumerate() {
        println!("cargo::rerun-if-changed={}", path.display());
        let bytes = fs::read(path).expect("read asset");
        let route = format!(
            "/{}",
            path.strip_prefix(&dist)
                .expect("inside dist")
                .to_string_lossy()
                .replace('\\', "/")
        );
        let ext = path
            .extension()
            .and_then(|e| e.to_str())
            .unwrap_or_default();
        let (mut br, mut zst) = ("None".to_owned(), "None".to_owned());
        if COMPRESSIBLE.contains(&ext) && bytes.len() >= MIN_COMPRESS_BYTES {
            let mut compressed = Vec::new();
            let params = brotli::enc::BrotliEncoderParams {
                quality: 11,
                lgwin: 22,
                ..Default::default()
            };
            brotli::BrotliCompress(&mut bytes.as_slice(), &mut compressed, &params)
                .expect("brotli");
            let file = out_dir.join(format!("asset{i}.br"));
            fs::write(&file, &compressed).expect("write br");
            br = format!("Some(include_bytes!({:?}))", file.display().to_string());
            let compressed = zstd::bulk::compress(&bytes, 19).expect("zstd");
            let file = out_dir.join(format!("asset{i}.zst"));
            fs::write(&file, &compressed).expect("write zst");
            zst = format!("Some(include_bytes!({:?}))", file.display().to_string());
        }
        let raw = fs::canonicalize(path).expect("canonical path");
        writeln!(
            code,
            "    Asset {{ path: {route:?}, mime: {:?}, etag: {:?}, raw: include_bytes!({:?}), br: {br}, zstd: {zst} }},",
            mime(path),
            fingerprint::etag(&bytes),
            raw.display().to_string(),
        )
        .expect("write code");
    }
    code.push(']');
    fs::write(out_dir.join("assets.rs"), code).expect("write assets.rs");

    let index = fs::read_to_string(dist.join("index.html")).unwrap_or_default();
    let hashes = csp::inline_script_hashes(&index);
    fs::write(out_dir.join("script_hashes.rs"), format!("&{hashes:?}"))
        .expect("write script_hashes.rs");
    let manifest = dist.join(".vite/manifest.json");
    println!("cargo::rerun-if-changed={}", manifest.display());
    let chunks =
        fs::read_to_string(&manifest).map_or_else(|_| BTreeMap::new(), |m| route_chunks(&m));
    fs::write(
        out_dir.join("pages.rs"),
        pages(&out_dir, index.as_bytes(), &chunks),
    )
    .expect("write pages.rs");
}

/// One chunk of Vite's manifest.
#[derive(serde::Deserialize)]
struct Chunk {
    file: String,
    #[serde(default)]
    imports: Vec<String>,
    #[serde(default, rename = "isEntry")]
    is_entry: bool,
}

/// Each route's component code, split out by TanStack Router (`src/routes/<route>.tsx`): the
/// chunk and every chunk it imports, less those index.html already loads, as URLs.
fn route_chunks(manifest: &str) -> BTreeMap<String, Vec<String>> {
    let chunks: BTreeMap<String, Chunk> = serde_json::from_str(manifest).expect("vite manifest");
    let closure = |key: &str| {
        let mut seen = BTreeSet::new();
        let mut stack = vec![key.to_owned()];
        while let Some(key) = stack.pop() {
            if let Some(chunk) = chunks.get(&key)
                && seen.insert(key)
            {
                stack.extend(chunk.imports.iter().cloned());
            }
        }
        seen
    };
    let loaded: BTreeSet<String> = chunks
        .iter()
        .filter(|(_, c)| c.is_entry)
        .flat_map(|(key, _)| closure(key))
        .collect();
    chunks
        .keys()
        .filter_map(|key| {
            let route = key
                .strip_prefix("src/routes/")?
                .strip_suffix(".tsx?tsr-split=component")?;
            let mut files: Vec<String> = closure(key)
                .difference(&loaded)
                .map(|k| format!("/{}", chunks[k].file))
                .collect();
            // The route's own chunk first.
            files.sort_by_key(|f| *f != format!("/{}", chunks[key].file));
            Some((route.to_owned(), files))
        })
        .collect()
}

/// index.html for each route (and one for any other path), cut before `</body>`: the part
/// before, with `<link rel="modulepreload">` tags for the route's code added, both as is and
/// compressed but left open (flushed, so it ends on a byte boundary, not finished), so that a
/// response appends the page's data preloads and the rest as stored data and ends the stream.
fn pages(out_dir: &Path, html: &[u8], chunks: &BTreeMap<String, Vec<String>>) -> String {
    let Some(at) = html
        .windows(PRELOADS_AT.len())
        .position(|w| w == PRELOADS_AT)
    else {
        return "Pages { tail: b\"\", routes: &[] }".to_owned();
    };
    let (head, tail) = html.split_at(at);
    let tail_file = out_dir.join("page-tail");
    fs::write(&tail_file, tail).expect("write page tail");
    let no_code = Vec::new();
    let mut routes = String::new();
    for (route, files) in
        std::iter::once(("", &no_code)).chain(chunks.iter().map(|(r, f)| (r.as_str(), f)))
    {
        let mut page = head.to_vec();
        for file in files {
            write!(
                page,
                r#"<link rel="modulepreload" crossorigin href="{file}">"#
            )
            .expect("write");
        }

        let mut brotli = brotli::CompressorWriter::new(Vec::new(), 4096, 11, 22);
        brotli.write_all(&page).expect("brotli");
        brotli.flush().expect("brotli flush");
        let br = brotli.get_ref().clone();

        let mut zstd = zstd::stream::write::Encoder::new(Vec::new(), 19).expect("zstd");
        // The frame's length is unknown here, and a checksum would cover the appended part too.
        zstd.include_contentsize(false).expect("zstd");
        zstd.include_checksum(false).expect("zstd");
        zstd.write_all(&page).expect("zstd");
        zstd.flush().expect("zstd flush");
        let zst = zstd.get_ref().clone();

        let mut fields = String::new();
        for (name, bytes) in [("head", &page), ("br_head", &br), ("zstd_head", &zst)] {
            let file = out_dir.join(format!("page-{}-{name}", route.replace('$', "_")));
            fs::write(&file, bytes).expect("write page part");
            write!(
                fields,
                "{name}: include_bytes!({:?}), ",
                file.display().to_string()
            )
            .expect("write code");
        }
        write!(routes, "({route:?}, Page {{ {fields}}}), ").expect("write code");
    }
    format!(
        "Pages {{ tail: include_bytes!({:?}), routes: &[{routes}] }}",
        tail_file.display().to_string()
    )
}
