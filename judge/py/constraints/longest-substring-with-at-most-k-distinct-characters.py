"""Longest Substring with At Most K Distinct Characters: a string and k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert 0 <= k <= 50, "0 <= k <= 50"
