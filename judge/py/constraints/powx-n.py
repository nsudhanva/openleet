"""Pow(x, n): a real base and an integer exponent."""

from math import log10


def check(x: float, n: int) -> None:
    assert isinstance(n, int) and not isinstance(n, bool), "n is an integer"
    assert -100.0 < x < 100.0, "-100.0 < x < 100.0"
    assert -(2**31) <= n <= 2**31 - 1, "-2^31 <= n <= 2^31 - 1"
    assert x != 0 or n > 0, "either x is not zero or n > 0"
    if x != 0:
        assert n * log10(abs(x)) <= 4 + 1e-9, "-10^4 <= x^n <= 10^4"
