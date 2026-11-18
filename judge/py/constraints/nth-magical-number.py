"""Nth Magical Number: the integers n, a and b."""


def check(n: int, a: int, b: int) -> None:
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert 2 <= a <= 4 * 10**4 and 2 <= b <= 4 * 10**4, "2 <= a, b <= 4 * 10^4"
