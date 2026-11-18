"""Minimum Absolute Difference in Sliding Submatrix: an m x n integer grid and a window size k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 30, "1 <= m <= 30"
    n = len(grid[0])
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(-(10**5) <= v <= 10**5 for row in grid for v in row), "-10^5 <= grid[i][j] <= 10^5"
    assert 1 <= k <= min(m, n), "1 <= k <= min(m, n)"
