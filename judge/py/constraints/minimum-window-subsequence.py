"""Minimum Window Subsequence: two lowercase strings."""


def check(s1: str, s2: str) -> None:
    assert 1 <= len(s1) <= 2 * 10**4, "1 <= s1.length <= 2 * 10^4"
    assert 1 <= len(s2) <= 100, "1 <= s2.length <= 100"
    assert all("a" <= c <= "z" for c in s1), "s1 consists of lowercase English letters"
    assert all("a" <= c <= "z" for c in s2), "s2 consists of lowercase English letters"
