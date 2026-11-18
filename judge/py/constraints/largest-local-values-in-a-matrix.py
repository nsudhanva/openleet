"""Largest Local Values in a Matrix: an n x n grid of small positive integers."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 3 <= n <= 100, "3 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(1 <= v <= 100 for row in grid for v in row), "1 <= grid[i][j] <= 100"
