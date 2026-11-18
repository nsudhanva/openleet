"""Longest Subsequence Repeated k Times: a lowercase string and a repeat count k."""


def check(s: str, k: int) -> None:
    n = len(s)
    assert 2 <= k <= 2000, "2 <= k <= 2000"
    assert 2 <= n < min(2001, k * 8), "2 <= n < min(2001, k * 8)"
    assert all(c.isascii() and c.isalpha() and c.islower() for c in s), (
        "s consists of lowercase English letters"
    )
