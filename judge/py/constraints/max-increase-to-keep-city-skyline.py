"""Max Increase to Keep City Skyline: an n x n grid of building heights."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 2 <= n <= 50, "2 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[r].length"
    assert all(0 <= v <= 100 for row in grid for v in row), "0 <= grid[r][c] <= 100"
