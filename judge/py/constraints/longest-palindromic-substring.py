"""Longest Palindromic Substring: a string of digits and English letters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c.isascii() and c.isalnum() for c in s), (
        "s consist of only digits and English letters"
    )
