//! The hashes that let the web app's inline scripts run under the Content-Security-Policy.
//! Shared with build.rs, which hashes the embedded index.html, so the policy always matches
//! the build.

use base64::Engine as _;
use sha2::{Digest, Sha256};

/// The `'sha256-...'` source of every inline `<script>` (one without `src`) in `html`, in
/// order. The hash covers exactly the text between the tags, as browsers compute it.
#[must_use]
pub fn inline_script_hashes(html: &str) -> Vec<String> {
    let mut hashes = Vec::new();
    let mut rest = html;
    while let Some(start) = rest.find("<script") {
        let Some(open_end) = rest[start..].find('>').map(|i| start + i + 1) else {
            break;
        };
        let Some(close) = rest[open_end..].find("</script>").map(|i| open_end + i) else {
            break;
        };
        if !rest[start..open_end].contains("src=") {
            let digest = Sha256::digest(&rest.as_bytes()[open_end..close]);
            let encoded = base64::engine::general_purpose::STANDARD.encode(digest);
            hashes.push(format!("'sha256-{encoded}'"));
        }
        rest = &rest[close..];
    }
    hashes
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hashes_only_inline_scripts() {
        let html = r#"<head><script type="module" src="/a.js"></script>
            <script>alert(1)</script></head>"#;
        // printf 'alert(1)' | openssl dgst -sha256 -binary | base64
        assert_eq!(
            inline_script_hashes(html),
            ["'sha256-bhHHL3z2vDgxUt0W3dWQOrprscmda2Y5pLsLg4GF+pI='"]
        );
        assert_eq!(
            inline_script_hashes("<p>no scripts</p>"),
            Vec::<String>::new()
        );
    }
}
