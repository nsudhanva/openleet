//! Compares a solution's answer with the expected one, the way openleet.judging.assemble chose
//! when it built the tests (keep the two in step).

use std::borrow::Cow;
use std::fmt::Write as _;

use openleet_proto::Checker;
use serde_json::Value;
use sha2::{Digest, Sha256};

/// The official judge accepts floating-point answers within 1e-5.
const TOLERANCE: f64 = 1e-5;

/// Whether `actual` is an accepted answer for `expected`.
#[must_use]
pub fn accepts(checker: Checker, floats: bool, actual: &Value, expected: &Value) -> bool {
    let (actual, expected) = (normalize(checker, actual), normalize(checker, expected));
    if floats {
        close(&actual, &expected)
    } else {
        actual == expected
    }
}

/// Whether the answer's exact JSON text, as the child printed it, hashes to `sha256_hex`.
#[must_use]
pub fn digest_matches(raw: &str, sha256_hex: &str) -> bool {
    let digest = Sha256::digest(raw.as_bytes());
    let mut hex = String::with_capacity(digest.len() * 2);
    for byte in digest {
        // Writing to a String cannot fail.
        let _ = write!(hex, "{byte:02x}");
    }
    hex.eq_ignore_ascii_case(sha256_hex)
}

/// The form two answers must share: lists sorted where order does not matter.
fn normalize(checker: Checker, value: &Value) -> Cow<'_, Value> {
    let Value::Array(items) = value else {
        return Cow::Borrowed(value);
    };
    match checker {
        Checker::Exact => Cow::Borrowed(value),
        Checker::Unordered => Cow::Owned(sorted(items.clone())),
        Checker::UnorderedNested => Cow::Owned(sorted(
            items
                .iter()
                .map(|item| match item {
                    Value::Array(inner) => sorted(inner.clone()),
                    other => other.clone(),
                })
                .collect(),
        )),
    }
}

/// Sorts by compact JSON text with sorted keys, like assemble.key.
fn sorted(mut items: Vec<Value>) -> Value {
    items.sort_by_cached_key(ToString::to_string);
    Value::Array(items)
}

fn close(a: &Value, b: &Value) -> bool {
    match (a, b) {
        (Value::Number(x), Value::Number(y)) => match (x.as_f64(), y.as_f64()) {
            (Some(x), Some(y)) => {
                let diff = (x - y).abs();
                diff <= TOLERANCE || diff <= TOLERANCE * x.abs().max(y.abs())
            }
            _ => x == y,
        },
        (Value::Array(x), Value::Array(y)) => {
            x.len() == y.len() && x.iter().zip(y).all(|(x, y)| close(x, y))
        }
        _ => a == b,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn exact(actual: &Value, expected: &Value) -> bool {
        accepts(Checker::Exact, false, actual, expected)
    }

    #[test]
    fn exact_needs_same_order() {
        assert!(exact(&json!([0, 1]), &json!([0, 1])));
        assert!(!exact(&json!([1, 0]), &json!([0, 1])));
        assert!(!exact(&json!(1), &json!(true)));
        assert!(!exact(&json!(1), &json!(1.0)));
    }

    #[test]
    fn objects_ignore_key_order() {
        let a: Value = serde_json::from_str(r#"{"a":1,"b":[2]}"#).unwrap();
        let b: Value = serde_json::from_str(r#"{"b":[2],"a":1}"#).unwrap();
        assert!(exact(&a, &b));
    }

    #[test]
    fn unordered_sorts_one_level() {
        let unordered = |a: &Value, b: &Value| accepts(Checker::Unordered, false, a, b);
        assert!(unordered(&json!([1, 0]), &json!([0, 1])));
        assert!(!unordered(&json!([[2, 1]]), &json!([[1, 2]])));
        assert!(!unordered(&json!([0, 0, 1]), &json!([0, 1, 1])));
        assert!(unordered(&json!("ab"), &json!("ab")));
    }

    #[test]
    fn unordered_nested_sorts_both_levels() {
        let nested = |a: &Value, b: &Value| accepts(Checker::UnorderedNested, false, a, b);
        assert!(nested(
            &json!([["b", "a"], ["c"]]),
            &json!([["c"], ["a", "b"]])
        ));
        assert!(nested(&json!([3, [2, 1]]), &json!([[1, 2], 3])));
        assert!(!nested(&json!([[1, 2]]), &json!([[1, 2, 2]])));
    }

    #[test]
    fn floats_within_tolerance() {
        let floats = |a: &Value, b: &Value| accepts(Checker::Exact, true, a, b);
        assert!(floats(&json!(2.000_001), &json!(2.0)));
        assert!(floats(&json!(2), &json!(2.0)));
        assert!(!floats(&json!(2.001), &json!(2.0)));
        assert!(floats(&json!(1_000_000.0), &json!(1_000_005.0)));
        assert!(floats(&json!([null, 1.000_001]), &json!([null, 1.0])));
        assert!(!floats(&json!([1.0]), &json!([1.0, 1.0])));
        assert!(!floats(&json!(true), &json!(1.0)));
    }

    #[test]
    fn floats_with_unordered() {
        assert!(accepts(
            Checker::Unordered,
            true,
            &json!([2.000_001, 1.0]),
            &json!([1.0, 2.0])
        ));
    }

    #[test]
    fn digest_of_the_exact_text() {
        // From `shasum -a 256` and Python's
        // hashlib.sha256(json.dumps(v, separators=(",", ":"), ensure_ascii=False).encode()).
        let pair = "49a64717d5d4cb19952e6eac2946415cf6879adacf9908e7d872332d32c6e684";
        let unicode = "50f42003d4ea3d90e8fc5d170ffc70daa4d284a5d11e3622f362b237a7a28349";
        assert!(digest_matches("[1,2]", pair));
        assert!(digest_matches("[1,2]", &pair.to_uppercase()));
        assert!(digest_matches(r#"[[1,2],"é",null]"#, unicode));
        assert!(!digest_matches("[1, 2]", pair));
        assert!(!digest_matches("[2,1]", pair));
        assert!(!digest_matches("[1,2]", ""));
    }

    #[test]
    fn big_integers_compare_exactly() {
        let big: Value = serde_json::from_str("123456789012345678901234567890").unwrap();
        let other: Value = serde_json::from_str("123456789012345678901234567891").unwrap();
        assert!(!exact(&big, &other));
        assert!(exact(&big, &big.clone()));
    }
}
