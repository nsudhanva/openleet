"""Largest Number After Digit Swaps by Parity: a positive integer."""


def check(num: int) -> None:
    assert isinstance(num, int), "num is an integer"
    assert 1 <= num <= 10**9, "1 <= num <= 10^9"
