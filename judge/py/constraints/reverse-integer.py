"""Reverse Integer: a signed 32-bit integer."""


def check(x: int) -> None:
    assert isinstance(x, int), "x is an integer"
    assert -(2**31) <= x <= 2**31 - 1, "-2^31 <= x <= 2^31 - 1"
