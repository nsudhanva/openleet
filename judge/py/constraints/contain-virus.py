"""Contain Virus: an m x n grid of 0/1 cells."""


def check(isInfected: list[list[int]]) -> None:
    m = len(isInfected)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(isInfected[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in isInfected), "n == isInfected[i].length"
    assert all(v in (0, 1) for row in isInfected for v in row), "isInfected[i][j] is either 0 or 1"
