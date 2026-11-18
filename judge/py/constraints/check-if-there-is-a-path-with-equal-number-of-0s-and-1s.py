"""Check if There is a Path With Equal Number of 0's And 1's: an m x n binary grid."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 2 <= m <= 100, "2 <= m <= 100"
    n = len(grid[0])
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
