"""Zigzag Grid Traversal With Skip: an n x m grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 2 <= n <= 50, "2 <= n == grid.length <= 50"
    m = len(grid[0])
    assert 2 <= m <= 50, "2 <= m == grid[i].length <= 50"
    assert all(len(row) == m for row in grid), "m == grid[i].length"
    assert all(1 <= v <= 2500 for row in grid for v in row), "1 <= grid[i][j] <= 2500"
