"""Smallest Subsequence of Distinct Characters: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
