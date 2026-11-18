"""Unique Paths: grid dimensions m and n."""

from math import comb


def check(m: int, n: int) -> None:
    assert isinstance(m, int) and isinstance(n, int), "m and n are integers"
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert comb(m + n - 2, m - 1) <= 2 * 10**9, "the answer is at most 2 * 10^9"
