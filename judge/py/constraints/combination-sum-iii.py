"""Combination Sum III: k numbers from 1..9 and a sum n."""


def check(k: int, n: int) -> None:
    assert 2 <= k <= 9, "2 <= k <= 9"
    assert 1 <= n <= 60, "1 <= n <= 60"
