"""Where Will the Ball Fall: an m x n grid of 1 and -1 diagonal boards."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (1, -1) for row in grid for v in row), "grid[i][j] is 1 or -1"
