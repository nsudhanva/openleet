"""Swim in Rising Water: an n x n grid of unique elevations."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    values = [v for row in grid for v in row]
    assert all(0 <= v < n * n for v in values), "0 <= grid[i][j] < n^2"
    assert len(set(values)) == len(values), "each value grid[i][j] is unique"
