"""Surface Area of 3D Shapes: an n x n grid of tower heights."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(0 <= v <= 50 for row in grid for v in row), "0 <= grid[i][j] <= 50"
