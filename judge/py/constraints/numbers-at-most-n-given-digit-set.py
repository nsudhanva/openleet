"""Numbers At Most N Given Digit Set: sorted unique digit characters 1-9 and a bound n."""


def check(digits: list[str], n: int) -> None:
    assert 1 <= len(digits) <= 9, "1 <= digits.length <= 9"
    assert all(isinstance(d, str) and len(d) == 1 for d in digits), "digits[i].length == 1"
    assert all(d in "123456789" for d in digits), "digits[i] is a digit from '1' to '9'"
    assert len(set(digits)) == len(digits), "all the values in digits are unique"
    assert digits == sorted(digits), "digits is sorted in non-decreasing order"
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
