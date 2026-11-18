"""Regions Cut By Slashes: an n x n grid of strings made of '/', '\\' and ' '."""


def check(grid: list[str]) -> None:
    n = len(grid)
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert all(isinstance(row, str) and len(row) == n for row in grid), (
        "n == grid.length == grid[i].length"
    )
    assert all(c in "/\\ " for row in grid for c in row), "grid[i][j] is either '/', '\\', or ' '"
