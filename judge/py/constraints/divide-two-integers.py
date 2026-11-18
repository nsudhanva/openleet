"""Divide Two Integers: a dividend and a nonzero divisor."""


def check(dividend: int, divisor: int) -> None:
    assert isinstance(dividend, int) and isinstance(divisor, int), "integers"
    assert -(2**31) <= dividend <= 2**31 - 1, "-2^31 <= dividend <= 2^31 - 1"
    assert -(2**31) <= divisor <= 2**31 - 1, "-2^31 <= divisor <= 2^31 - 1"
    assert divisor != 0, "divisor != 0"
