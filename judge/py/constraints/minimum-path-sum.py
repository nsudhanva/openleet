"""Minimum Path Sum: an m x n grid of non-negative ints."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(grid[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(0 <= v <= 200 for row in grid for v in row), "0 <= grid[i][j] <= 200"
