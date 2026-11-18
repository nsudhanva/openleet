"""Construct Product Matrix: an n x m grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert n >= 1 and isinstance(grid[0], list), "grid is a matrix"
    assert 1 <= n <= 10**5, "1 <= n == grid.length <= 10^5"
    m = len(grid[0])
    assert 1 <= m <= 10**5, "1 <= m == grid[i].length <= 10^5"
    assert all(len(row) == m for row in grid), "m == grid[i].length"
    assert 2 <= n * m <= 10**5, "2 <= n * m <= 10^5"
    assert all(1 <= v <= 10**9 for row in grid for v in row), "1 <= grid[i][j] <= 10^9"
