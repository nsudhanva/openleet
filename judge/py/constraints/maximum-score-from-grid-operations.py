"""Maximum Score From Grid Operations: an n x n grid of non-negative integers."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 100, "1 <= n == grid.length <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(0 <= v <= 10**9 for row in grid for v in row), "0 <= grid[i][j] <= 10^9"
