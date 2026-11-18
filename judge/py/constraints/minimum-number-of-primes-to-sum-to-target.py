"""Minimum Number of Primes to Sum to Target: two integers n and m."""


def check(n: int, m: int) -> None:
    assert isinstance(n, int) and 1 <= n <= 1000, "1 <= n <= 1000"
    assert isinstance(m, int) and 1 <= m <= 1000, "1 <= m <= 1000"
