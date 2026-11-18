"""Longest Duplicate Substring: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 3 * 10**4, "2 <= s.length <= 3 * 10^4"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
