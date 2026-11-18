"""Rotting Oranges: an m x n grid of 0, 1 and 2."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 10, "1 <= m <= 10"
    n = len(grid[0])
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(v in (0, 1, 2) for r in grid for v in r), "grid[i][j] is 0, 1, or 2"
