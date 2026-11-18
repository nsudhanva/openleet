"""Maximize Sum of Device Ratings: an m x n matrix of unit capacities."""


def check(units: list[list[int]]) -> None:
    m = len(units)
    assert 1 <= m <= 10**5, "1 <= m == units.length <= 10^5"
    n = len(units[0])
    assert 1 <= n <= 10**5, "1 <= n == units[i].length <= 10^5"
    assert all(len(row) == n for row in units), "n == units[i].length"
    assert m * n <= 2 * 10**5, "m * n <= 2 * 10^5"
    assert all(1 <= v <= 10**5 for row in units for v in row), "1 <= units[i][j] <= 10^5"
