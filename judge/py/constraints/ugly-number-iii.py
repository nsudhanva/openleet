"""Ugly Number III: n and three divisors a, b, c."""

from math import gcd


def check(n: int, a: int, b: int, c: int) -> None:
    assert all(1 <= v <= 10**9 for v in (n, a, b, c)), "1 <= n, a, b, c <= 10^9"
    assert 1 <= a * b * c <= 10**18, "1 <= a * b * c <= 10^18"

    def lcm(x: int, y: int) -> int:
        return x // gcd(x, y) * y

    ab, ac, bc = lcm(a, b), lcm(a, c), lcm(b, c)
    abc = lcm(ab, c)
    limit = 2 * 10**9

    def count(x: int) -> int:
        return x // a + x // b + x // c - x // ab - x // ac - x // bc + x // abc

    assert count(limit) >= n, "the result is in range [1, 2 * 10^9]"
