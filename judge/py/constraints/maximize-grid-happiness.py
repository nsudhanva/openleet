"""Maximize Grid Happiness: grid size and counts of introverts and extroverts."""


def check(m: int, n: int, introvertsCount: int, extrovertsCount: int) -> None:
    assert 1 <= m <= 5 and 1 <= n <= 5, "1 <= m, n <= 5"
    cap = min(m * n, 6)
    assert 0 <= introvertsCount <= cap, "0 <= introvertsCount <= min(m * n, 6)"
    assert 0 <= extrovertsCount <= cap, "0 <= extrovertsCount <= min(m * n, 6)"
