"""Defuse the Bomb: a circular array of positive integers and a shift k."""


def check(code: list[int], k: int) -> None:
    n = len(code)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= v <= 100 for v in code), "1 <= code[i] <= 100"
    assert -(n - 1) <= k <= n - 1, "-(n - 1) <= k <= n - 1"
