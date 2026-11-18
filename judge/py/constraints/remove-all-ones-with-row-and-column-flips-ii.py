"""Remove All Ones With Row and Column Flips II: an m x n binary grid with at most 15 cells."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 15, "1 <= m <= 15"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= n <= 15, "1 <= n <= 15"
    assert 1 <= m * n <= 15, "1 <= m * n <= 15"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
