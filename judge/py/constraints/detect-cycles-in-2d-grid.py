"""Detect Cycles in 2D Grid: an m x n grid of lowercase letters."""


def check(grid: list[list[str]]) -> None:
    m = len(grid)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(grid[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(
        isinstance(c, str) and len(c) == 1 and "a" <= c <= "z" for row in grid for c in row
    ), "grid consists only of lowercase English letters"
