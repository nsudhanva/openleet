"""Largest 1-Bordered Square: a rectangular grid of 0s and 1s."""


def check(grid: list[list[int]]) -> None:
    assert 1 <= len(grid) <= 100, "1 <= grid.length <= 100"
    assert 1 <= len(grid[0]) <= 100, "1 <= grid[0].length <= 100"
    assert all(len(row) == len(grid[0]) for row in grid), "grid is rectangular"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is 0 or 1"
