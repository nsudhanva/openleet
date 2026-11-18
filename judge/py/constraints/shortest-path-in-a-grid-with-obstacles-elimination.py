"""Shortest Path in a Grid with Obstacles Elimination: a 0/1 grid and a budget k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 40, "1 <= m <= 40"
    n = len(grid[0])
    assert 1 <= n <= 40, "1 <= n <= 40"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= k <= m * n, "1 <= k <= m * n"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert grid[0][0] == grid[m - 1][n - 1] == 0, "grid[0][0] == grid[m - 1][n - 1] == 0"
