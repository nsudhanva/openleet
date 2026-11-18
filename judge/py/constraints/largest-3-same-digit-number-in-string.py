"""Largest 3-Same-Digit Number in String: a string of digits."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 3 <= len(num) <= 1000, "3 <= num.length <= 1000"
