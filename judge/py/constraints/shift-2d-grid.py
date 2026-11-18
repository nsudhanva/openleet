"""Shift 2D Grid: an m x n grid of integers and a shift count k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(-1000 <= v <= 1000 for row in grid for v in row), "-1000 <= grid[i][j] <= 1000"
    assert 0 <= k <= 100, "0 <= k <= 100"
