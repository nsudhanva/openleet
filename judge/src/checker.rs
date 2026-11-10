//! Compares a solution's answer with the expected one, the way openleet.judging.assemble chose
//! when it built the tests (keep the two in step).

use openleet_proto::Checker;
use serde_json::Value;

/// LeetCode accepts floating-point answers within 1e-5.
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

/// The form two answers must share: lists sorted where order does not matter.
fn normalize(checker: Checker, value: &Value) -> Value {
    let Value::Array(items) = value else {
        return value.clone();
    };
    let mut items = match checker {
        Checker::Exact => return value.clone(),
        Checker::Unordered => items.clone(),
        Checker::UnorderedNested => items.iter().map(sorted_if_list).collect(),
    };
    sort(&mut items);
    Value::Array(items)
}

fn sorted_if_list(value: &Value) -> Value {
    match value {
        Value::Array(items) => {
            let mut items = items.clone();
            sort(&mut items);
            Value::Array(items)
        }
        other => other.clone(),
    }
}

/// Sorts by canonical JSON text, the same key the Python side uses (keys sorted, compact).
fn sort(items: &mut [Value]) {
    items.sort_by_cached_key(|v| v.to_string());
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

    #[test]
    fn exact_needs_same_order() {
        assert!(accepts(
            Checker::Exact,
            false,
            &json!([0, 1]),
            &json!([0, 1])
        ));
        assert!(!accepts(
            Checker::Exact,
            false,
            &json!([1, 0]),
            &json!([0, 1])
        ));
        assert!(!accepts(Checker::Exact, false, &json!(1), &json!(true)));
    }

    #[test]
    fn unordered_sorts_one_level() {
        assert!(accepts(
            Checker::Unordered,
            false,
            &json!([1, 0]),
            &json!([0, 1])
        ));
        assert!(!accepts(
            Checker::Unordered,
            false,
            &json!([[2, 1]]),
            &json!([[1, 2]])
        ));
        assert!(accepts(
            Checker::UnorderedNested,
            false,
            &json!([["b", "a"], ["c"]]),
            &json!([["c"], ["a", "b"]])
        ));
    }

    #[test]
    fn floats_within_tolerance() {
        assert!(accepts(
            Checker::Exact,
            true,
            &json!(2.000_001),
            &json!(2.0)
        ));
        assert!(accepts(Checker::Exact, true, &json!(2), &json!(2.0)));
        assert!(!accepts(Checker::Exact, true, &json!(2.001), &json!(2.0)));
        assert!(accepts(
            Checker::Exact,
            true,
            &json!([null, 1.000_001]),
            &json!([null, 1.0])
        ));
    }

    #[test]
    fn big_integers_compare_exactly() {
        let big: Value = serde_json::from_str("123456789012345678901234567890").unwrap();
        let other: Value = serde_json::from_str("123456789012345678901234567891").unwrap();
        assert!(!accepts(Checker::Exact, false, &big, &other));
        assert!(accepts(Checker::Exact, false, &big, &big.clone()));
    }
}
