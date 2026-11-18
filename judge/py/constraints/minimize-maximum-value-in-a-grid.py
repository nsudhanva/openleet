"""Minimize Maximum Value in a Grid: an m x n matrix of distinct positive integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    values = [v for row in grid for v in row]
    assert all(1 <= v <= 10**9 for v in values), "1 <= grid[i][j] <= 10^9"
    assert len(set(values)) == len(values), "grid consists of distinct integers"
