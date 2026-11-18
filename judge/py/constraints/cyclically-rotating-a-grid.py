"""Cyclically Rotating a Grid: an m x n grid with m and n even, and a rotation count k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 2 <= m <= 50, "2 <= m <= 50"
    n = len(grid[0])
    assert 2 <= n <= 50, "2 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert m % 2 == 0 and n % 2 == 0, "both m and n are even"
    assert all(1 <= v <= 5000 for row in grid for v in row), "1 <= grid[i][j] <= 5000"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
