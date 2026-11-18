"""Divisor Game: the starting number n."""


def check(n: int) -> None:
    assert isinstance(n, int), "integer"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
