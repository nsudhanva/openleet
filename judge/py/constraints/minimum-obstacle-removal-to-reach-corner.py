"""Minimum Obstacle Removal to Reach Corner: an m x n grid of 0 (empty) and 1 (obstacle)."""


def check(grid: list[list[int]]) -> None:
    assert isinstance(grid, list) and grid, "grid is a non-empty list"
    m = len(grid)
    assert all(isinstance(r, list) for r in grid), "grid rows are lists"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= m <= 10**5 and 1 <= n <= 10**5, "1 <= m, n <= 10^5"
    assert 2 <= m * n <= 10**5, "2 <= m * n <= 10^5"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is either 0 or 1"
    assert grid[0][0] == 0 and grid[m - 1][n - 1] == 0, "grid[0][0] == grid[m - 1][n - 1] == 0"
