"""Unique Length-3 Palindromic Subsequences: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 3 <= len(s) <= 10**5, "3 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
