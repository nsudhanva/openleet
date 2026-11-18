"""Palindrome Number: a 32-bit signed integer."""


def check(x: int) -> None:
    assert isinstance(x, int), "x is an integer"
    assert -(2**31) <= x <= 2**31 - 1, "-2^31 <= x <= 2^31 - 1"
