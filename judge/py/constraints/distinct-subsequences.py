"""Distinct Subsequences: two strings of English letters."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert 1 <= len(t) <= 1000, "1 <= t.length <= 1000"
    assert s.isascii() and s.isalpha(), "s consists of English letters"
    assert t.isascii() and t.isalpha(), "t consists of English letters"
