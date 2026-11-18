"""Coloring A Border: an m x n grid of colors, a start cell and a new color."""


def check(grid: list[list[int]], row: int, col: int, color: int) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    assert m >= 1, "grid is not empty"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(1 <= v <= 1000 for r in grid for v in r), "1 <= grid[i][j] <= 1000"
    assert 1 <= color <= 1000, "1 <= color <= 1000"
    assert 0 <= row < m, "0 <= row < m"
    assert 0 <= col < n, "0 <= col < n"
