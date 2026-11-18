"""Divisible and Non-divisible Sums Difference: two positive integers n and m."""


def check(n: int, m: int) -> None:
    assert isinstance(n, int) and isinstance(m, int), "integers"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m <= 1000, "1 <= m <= 1000"
