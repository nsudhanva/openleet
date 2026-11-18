"""Nim Game: the number of stones n."""


def check(n: int) -> None:
    assert 1 <= n <= 2**31 - 1, "1 <= n <= 2^31 - 1"
