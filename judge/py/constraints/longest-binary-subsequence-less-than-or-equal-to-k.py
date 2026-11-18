"""Longest Binary Subsequence Less Than or Equal to K: a binary string and a bound."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
