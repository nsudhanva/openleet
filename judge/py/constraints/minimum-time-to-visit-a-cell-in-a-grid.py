"""Minimum Time to Visit a Cell In a Grid: an m x n grid of earliest-visit times."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 2 <= m <= 1000, "2 <= m <= 1000"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 4 <= m * n <= 10**5, "4 <= m * n <= 10^5"
    assert all(0 <= v <= 10**5 for row in grid for v in row), "0 <= grid[i][j] <= 10^5"
    assert grid[0][0] == 0, "grid[0][0] == 0"
