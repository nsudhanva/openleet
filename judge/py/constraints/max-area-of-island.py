"""Max Area of Island: an m x n grid of 0s and 1s."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    assert grid, "non-empty"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
