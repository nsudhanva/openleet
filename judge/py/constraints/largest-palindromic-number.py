"""Largest Palindromic Number: a string of digits."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 1 <= len(num) <= 10**5, "1 <= num.length <= 10^5"
    assert all(c in "0123456789" for c in num), "num consists of digits"
