"""Disconnect Path in a Binary Matrix by at Most One Flip: an m x n grid of 0s and 1s."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert grid[0][0] == grid[m - 1][n - 1] == 1, "grid[0][0] == grid[m - 1][n - 1] == 1"
