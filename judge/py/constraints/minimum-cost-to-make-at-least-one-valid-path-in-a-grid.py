"""Minimum Cost to Make at Least One Valid Path in a Grid: an m x n grid of direction signs 1..4."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(1 <= v <= 4 for row in grid for v in row), "1 <= grid[i][j] <= 4"
