"""Longest Substring with At Most Two Distinct Characters: an English-letter string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c.isascii() and c.isalpha() for c in s), "s consists of English letters"
