"""Number of Enclaves: an m x n 0/1 grid."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(grid[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
