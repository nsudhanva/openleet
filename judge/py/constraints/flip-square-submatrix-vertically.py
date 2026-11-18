"""Flip Square Submatrix Vertically: an m x n grid and a k x k submatrix at (x, y)."""


def check(grid: list[list[int]], x: int, y: int, k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(1 <= v <= 100 for row in grid for v in row), "1 <= grid[i][j] <= 100"
    assert 0 <= x < m, "0 <= x < m"
    assert 0 <= y < n, "0 <= y < n"
    assert 1 <= k <= min(m - x, n - y), "1 <= k <= min(m - x, n - y)"
