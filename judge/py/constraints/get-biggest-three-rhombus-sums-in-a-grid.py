"""Get Biggest Three Rhombus Sums in a Grid: an m x n grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(1 <= v <= 10**5 for row in grid for v in row), "1 <= grid[i][j] <= 10^5"
