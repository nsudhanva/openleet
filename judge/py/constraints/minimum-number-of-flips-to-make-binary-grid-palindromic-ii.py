"""Minimum Number of Flips to Make Binary Grid Palindromic II: an m x n binary grid."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert m >= 1, "m >= 1"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= m * n <= 2 * 10**5, "1 <= m * n <= 2 * 10^5"
    assert all(v in (0, 1) for row in grid for v in row), "0 <= grid[i][j] <= 1"
