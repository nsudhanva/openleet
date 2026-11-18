"""Convert a Number to Hexadecimal: a 32-bit signed integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert -(2**31) <= num <= 2**31 - 1, "-2^31 <= num <= 2^31 - 1"
