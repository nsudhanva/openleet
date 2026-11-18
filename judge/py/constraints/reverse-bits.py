"""Reverse Bits: an even 32-bit integer."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 0 <= n <= 2**31 - 2, "0 <= n <= 2^31 - 2"
    assert n % 2 == 0, "n is even"
