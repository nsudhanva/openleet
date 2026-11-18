"""Find the Width of Columns of a Grid: an m x n grid of integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(-(10**9) <= v <= 10**9 for row in grid for v in row), "-10^9 <= grid[r][c] <= 10^9"
