"""Complement of Base 10 Integer: one integer."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 0 <= n < 10**9, "0 <= n < 10^9"
