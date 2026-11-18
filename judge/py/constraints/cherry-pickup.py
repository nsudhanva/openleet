"""Cherry Pickup: an n x n grid of -1, 0, 1 with open corners."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(v in (-1, 0, 1) for row in grid for v in row), "grid[i][j] is -1, 0, or 1"
    assert grid[0][0] != -1, "grid[0][0] != -1"
    assert grid[n - 1][n - 1] != -1, "grid[n - 1][n - 1] != -1"
