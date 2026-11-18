"""Sqrt(x): a non-negative 32-bit integer."""


def check(x: int) -> None:
    assert isinstance(x, int), "x is an integer"
    assert 0 <= x <= 2**31 - 1, "0 <= x <= 2^31 - 1"
