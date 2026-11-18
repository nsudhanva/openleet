"""Difference Between Ones and Zeros in Row and Column: an m x n binary grid."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    n = len(grid[0])
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
