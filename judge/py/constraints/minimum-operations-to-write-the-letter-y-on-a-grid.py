"""Minimum Operations to Write the Letter Y on a Grid: an odd n x n grid of 0..2."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 3 <= n <= 49, "3 <= n <= 49"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert n % 2 == 1, "n is odd"
    assert all(0 <= v <= 2 for row in grid for v in row), "0 <= grid[i][j] <= 2"
