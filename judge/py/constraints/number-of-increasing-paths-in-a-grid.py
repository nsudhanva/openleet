"""Number of Increasing Paths in a Grid: a rectangular grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(1 <= v <= 10**5 for row in grid for v in row), "1 <= grid[i][j] <= 10^5"
