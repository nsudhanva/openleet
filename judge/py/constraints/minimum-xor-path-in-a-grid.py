"""Minimum XOR Path in a Grid: an m x n grid of integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m == grid.length <= 1000"
    assert grid and isinstance(grid[0], list), "grid is a non-empty matrix"
    n = len(grid[0])
    assert 1 <= n <= 1000, "1 <= n == grid[i].length <= 1000"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert m * n <= 1000, "m * n <= 1000"
    assert all(0 <= v <= 1023 for row in grid for v in row), "0 <= grid[i][j] <= 1023"
