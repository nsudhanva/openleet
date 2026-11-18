"""Powerful Integers: bases x, y and an upper bound."""


def check(x: int, y: int, bound: int) -> None:
    assert 1 <= x <= 100 and 1 <= y <= 100, "1 <= x, y <= 100"
    assert 0 <= bound <= 10**6, "0 <= bound <= 10^6"
