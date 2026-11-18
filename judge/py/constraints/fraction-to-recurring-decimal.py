"""Fraction to Recurring Decimal: a numerator and a non-zero denominator."""


def check(numerator: int, denominator: int) -> None:
    assert -(2**31) <= numerator <= 2**31 - 1, "-2^31 <= numerator <= 2^31 - 1"
    assert -(2**31) <= denominator <= 2**31 - 1, "-2^31 <= denominator <= 2^31 - 1"
    assert denominator != 0, "denominator != 0"
