"""Longest Palindrome: a string of English letters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2000, "1 <= s.length <= 2000"
    assert all(c.isascii() and c.isalpha() for c in s), (
        "s consists of lowercase and/or uppercase English letters only"
    )
