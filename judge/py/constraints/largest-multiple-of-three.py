"""Largest Multiple of Three: an array of decimal digits."""


def check(digits: list[int]) -> None:
    assert 1 <= len(digits) <= 10**4, "1 <= digits.length <= 10^4"
    assert all(0 <= d <= 9 for d in digits), "0 <= digits[i] <= 9"
