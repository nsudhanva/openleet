//! Content fingerprints: strong `ETag`s, and the seed of a plan's shuffle. Shared with
//! build.rs, which embeds the web app.

/// FNV-1a: fast, and enough to tell build outputs and data versions apart.
#[must_use]
pub fn fnv1a(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0xcbf2_9ce4_8422_2325, |hash, b| {
        (hash ^ u64::from(*b)).wrapping_mul(0x0100_0000_01b3)
    })
}

/// A strong `ETag` value for `bytes`, quotes included.
#[must_use]
pub fn etag(bytes: &[u8]) -> String {
    format!("\"{:016x}\"", fnv1a(bytes))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn matches_the_fnv1a_reference_values() {
        assert_eq!(fnv1a(b""), 0xcbf2_9ce4_8422_2325);
        assert_eq!(fnv1a(b"a"), 0xaf63_dc4c_8601_ec8c);
        assert_eq!(etag(b"a"), "\"af63dc4c8601ec8c\"");
    }
}
