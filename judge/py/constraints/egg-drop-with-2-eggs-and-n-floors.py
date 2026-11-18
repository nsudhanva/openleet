"""Egg Drop With 2 Eggs and N Floors: the number of floors n."""


def check(n: int) -> None:
    assert isinstance(n, int), "integer"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
