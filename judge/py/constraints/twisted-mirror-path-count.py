"""Twisted Mirror Path Count: an m x n grid of 0 (empty) and 1 (mirror)."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 2 <= m <= 500, "2 <= m <= 500"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 2 <= n <= 500, "2 <= n <= 500"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is either 0 or 1"
    assert grid[0][0] == grid[m - 1][n - 1] == 0, "grid[0][0] == grid[m - 1][n - 1] == 0"
