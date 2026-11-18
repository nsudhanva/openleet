"""Least Operators to Express Number: a base x and a target."""


def check(x: int, target: int) -> None:
    assert 2 <= x <= 100, "2 <= x <= 100"
    assert 1 <= target <= 2 * 10**8, "1 <= target <= 2 * 10^8"
