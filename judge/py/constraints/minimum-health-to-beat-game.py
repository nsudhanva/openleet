"""Minimum Health to Beat Game: per-level damage and an armor value."""


def check(damage: list[int], armor: int) -> None:
    assert 1 <= len(damage) <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= x <= 10**5 for x in damage), "0 <= damage[i] <= 10^5"
    assert 0 <= armor <= 10**5, "0 <= armor <= 10^5"
