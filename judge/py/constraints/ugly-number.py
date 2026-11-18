"""Ugly Number: a 32-bit integer."""


def check(n: int) -> None:
    assert -(2**31) <= n <= 2**31 - 1, "-2^31 <= n <= 2^31 - 1"
