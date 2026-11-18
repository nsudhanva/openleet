"""Maximum Number of Fish in a Grid: an m x n grid of fish counts."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 10, "1 <= m <= 10"
    n = len(grid[0])
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(0 <= v <= 10 for row in grid for v in row), "0 <= grid[i][j] <= 10"
