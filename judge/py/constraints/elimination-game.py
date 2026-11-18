"""Elimination Game: the list length n of 1..n."""


def check(n: int) -> None:
    assert isinstance(n, int), "integer"
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
