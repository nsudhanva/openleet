"""Longest Palindromic Subsequence: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
