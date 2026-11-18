"""Minimum Falling Path Sum: an n x n integer grid."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(-99 <= x <= 99 for row in grid for x in row), "-99 <= grid[i][j] <= 99"
