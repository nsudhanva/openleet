"""Kth Smallest Number in Multiplication Table: table dimensions m, n and rank k."""


def check(m: int, n: int, k: int) -> None:
    assert 1 <= m <= 3 * 10**4, "1 <= m <= 3 * 10^4"
    assert 1 <= n <= 3 * 10**4, "1 <= n <= 3 * 10^4"
    assert 1 <= k <= m * n, "1 <= k <= m * n"
