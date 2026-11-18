"""Check if There is a Valid Path in a Grid: an m x n grid of street types 1..6."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(grid[0])
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(1 <= v <= 6 for row in grid for v in row), "1 <= grid[i][j] <= 6"
