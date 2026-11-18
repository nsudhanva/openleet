"""Smallest Palindromic Rearrangement II: a palindromic lowercase string and k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert s == s[::-1], "s is palindromic"
    assert 1 <= k <= 10**6, "1 <= k <= 10^6"
