//! Embeds the built web app (web/dist) in the binary, compressed ahead of time with Brotli
//! (quality 11) and zstd (level 19), so serving a file costs no CPU at all, and hashes the
//! inline scripts of its index.html for the Content-Security-Policy (src/security.rs).

#[path = "src/csp.rs"]
mod csp;
#[path = "src/fingerprint.rs"]
mod fingerprint;

use std::fmt::Write as _;
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
}
