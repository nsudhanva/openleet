"""Add Digits: a non-negative 32-bit integer."""


def check(num: int) -> None:
    assert 0 <= num <= 2**31 - 1, "0 <= num <= 2^31 - 1"
