"""As Far from Land as Possible: an n x n grid of 0 (water) and 1 (land)."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is 0 or 1"
