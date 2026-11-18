"""Escape the Spreading Fire: an m x n grid of grass (0), fire (1) and walls (2)."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 2 <= m <= 300, "2 <= m <= 300"
    assert all(isinstance(row, list) for row in grid), "grid is a list of rows"
    n = len(grid[0])
    assert 2 <= n <= 300, "2 <= n <= 300"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 4 <= m * n <= 2 * 10**4, "4 <= m * n <= 2 * 10^4"
    assert all(v in (0, 1, 2) for row in grid for v in row), "grid[i][j] is either 0, 1, or 2"
    assert grid[0][0] == 0 and grid[m - 1][n - 1] == 0, "grid[0][0] == grid[m - 1][n - 1] == 0"
