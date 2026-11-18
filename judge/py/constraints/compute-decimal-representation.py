"""Compute Decimal Representation: one positive integer."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
