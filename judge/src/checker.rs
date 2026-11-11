//! Compares a solution's answer with the expected one, the way openleet.judging.assemble chose
//! when it built the tests (keep the two in step).

use std::cmp::Ordering;
use std::fmt::Write as _;

use openleet_proto::Checker;
use serde_json::{Number, Value};
use sha2::{Digest, Sha256};

/// The official judge accepts floating-point answers within 1e-5.
const TOLERANCE: f64 = 1e-5;

/// Whether `actual` is an accepted answer for `expected`.
#[cfg(test)]
#[must_use]
fn accepts(checker: Checker, floats: bool, actual: &Value, expected: &Value) -> bool {
    let (actual, expected) = (
        normalize(checker, actual.clone()),
        normalize(checker, expected.clone()),
    );
    accepts_normalized(floats, &actual, &expected)
}

/// Whether two answers that are already in checker form match.
#[must_use]
pub fn accepts_normalized(floats: bool, actual: &Value, expected: &Value) -> bool {
    if floats {
        close(actual, expected)
    } else {
        actual == expected
    }
}

/// The form two answers must share: lists sorted where order does not matter.
#[must_use]
pub fn normalize(checker: Checker, value: Value) -> Value {
    let Value::Array(items) = value else {
        return value;
    };
    match checker {
        Checker::Exact => Value::Array(items),
        Checker::Unordered => sorted(items),
        Checker::UnorderedNested => sorted(
            items
                .into_iter()
                .map(|item| match item {
                    Value::Array(inner) => sorted(inner),
                    other => other,
                })
                .collect(),
        ),
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

/// Sorts by a structural JSON order shared with assemble.structural_key.
fn sorted(mut items: Vec<Value>) -> Value {
    items.sort_by_cached_key(structural_key);
    Value::Array(items)
}

#[derive(Eq, PartialEq)]
enum StructuralKey {
    Null,
    Bool(bool),
    Number(NumberKey),
    String(String),
    Array(Vec<Self>),
    Object(Vec<(String, Self)>),
}

impl Ord for StructuralKey {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            (Self::Null, Self::Null) => Ordering::Equal,
            (Self::Null, _) => Ordering::Less,
            (_, Self::Null) => Ordering::Greater,
            (Self::Bool(a), Self::Bool(b)) => a.cmp(b),
            (Self::Bool(_), _) => Ordering::Less,
            (_, Self::Bool(_)) => Ordering::Greater,
            (Self::Number(a), Self::Number(b)) => a.cmp(b),
            (Self::Number(_), _) => Ordering::Less,
            (_, Self::Number(_)) => Ordering::Greater,
            (Self::String(a), Self::String(b)) => a.cmp(b),
            (Self::String(_), _) => Ordering::Less,
            (_, Self::String(_)) => Ordering::Greater,
            (Self::Array(a), Self::Array(b)) => a.cmp(b),
            (Self::Array(_), _) => Ordering::Less,
            (_, Self::Array(_)) => Ordering::Greater,
            (Self::Object(a), Self::Object(b)) => a.cmp(b),
        }
    }
}

impl PartialOrd for StructuralKey {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Eq, PartialEq)]
struct NumberKey {
    sign: i8,
    adjusted: i128,
    digits: String,
}

impl NumberKey {
    fn new(number: &Number) -> Self {
        let text = number.to_string();
        let (mantissa, exponent) =
            text.split_once(['e', 'E'])
                .map_or((text.as_str(), 0), |(mantissa, exponent)| {
                    (
                        mantissa,
                        exponent.parse().unwrap_or_else(|_| {
                            if exponent.starts_with('-') {
                                i128::MIN / 2
                            } else {
                                i128::MAX / 2
                            }
                        }),
                    )
                });
        let (sign, mantissa) = mantissa
            .strip_prefix('-')
            .map_or((1, mantissa), |unsigned| (-1, unsigned));
        let (whole, fraction) = mantissa.split_once('.').unwrap_or((mantissa, ""));
        let mut digits = format!("{whole}{fraction}");
        let leading = digits.len() - digits.trim_start_matches('0').len();
        if leading == digits.len() {
            return Self {
                sign: 0,
                adjusted: 0,
                digits: "0".into(),
            };
        }
        digits.drain(..leading);
        let trailing = digits.len() - digits.trim_end_matches('0').len();
        digits.truncate(digits.len() - trailing);
        let exponent = exponent
            .saturating_sub(fraction.len() as i128)
            .saturating_add(trailing as i128);
        let adjusted = exponent.saturating_add(digits.len() as i128);
        Self {
            sign,
            adjusted,
            digits,
        }
    }

    fn magnitude_cmp(&self, other: &Self) -> Ordering {
        self.adjusted
            .cmp(&other.adjusted)
            .then_with(|| self.digits.cmp(&other.digits))
    }
}

impl Ord for NumberKey {
    fn cmp(&self, other: &Self) -> Ordering {
        self.sign.cmp(&other.sign).then_with(|| match self.sign {
            -1 => self.magnitude_cmp(other).reverse(),
            0 => Ordering::Equal,
            _ => self.magnitude_cmp(other),
        })
    }
}

impl PartialOrd for NumberKey {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn structural_key(value: &Value) -> StructuralKey {
    match value {
        Value::Null => StructuralKey::Null,
        Value::Bool(value) => StructuralKey::Bool(*value),
        Value::Number(value) => StructuralKey::Number(NumberKey::new(value)),
        Value::String(value) => StructuralKey::String(value.clone()),
        Value::Array(values) => StructuralKey::Array(values.iter().map(structural_key).collect()),
        Value::Object(values) => {
            let mut values: Vec<_> = values.iter().collect();
            values.sort_by_key(|(key, _)| *key);
            StructuralKey::Object(
                values
                    .into_iter()
                    .map(|(key, value)| (key.clone(), structural_key(value)))
                    .collect(),
            )
        }
    }
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
            &json!([2.0, 10.000_01]),
            &json!([2.000_01, 9.999_99])
        ));
        assert!(accepts(
            Checker::UnorderedNested,
            true,
            &json!([[10.000_01, 2], [4.000_001, 3]]),
            &json!([[3, 4.000_002], [2.000_01, 9.999_99]])
        ));
    }

    #[test]
    fn structural_order_compares_numbers_numerically() {
        let normalized = normalize(Checker::Unordered, json!([10, 2.0, 2]));
        assert_eq!(normalized, json!([2.0, 2, 10]));
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
