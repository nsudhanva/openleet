"""Decode Ways: a string of digits."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert s.isascii() and s.isdigit(), "s contains only digits"
