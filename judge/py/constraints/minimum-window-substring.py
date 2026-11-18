"""Minimum Window Substring: two strings of English letters."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= m <= 10^5"
    assert 1 <= len(t) <= 10**5, "1 <= n <= 10^5"
    assert s.isascii() and s.isalpha(), "s consists of uppercase and lowercase English letters"
    assert t.isascii() and t.isalpha(), "t consists of uppercase and lowercase English letters"
