"""Power of Three: one 32-bit signed integer."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert -(2**31) <= n <= 2**31 - 1, "-2^31 <= n <= 2^31 - 1"
