"""Minimum Swaps to Arrange a Binary Grid: an n x n grid of 0s and 1s."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
