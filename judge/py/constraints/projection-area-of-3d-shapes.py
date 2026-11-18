"""Projection Area of 3D Shapes: an n x n grid of tower heights."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(isinstance(r, list) and len(r) == n for r in grid), (
        "n == grid.length == grid[i].length"
    )
    assert all(0 <= v <= 50 for r in grid for v in r), "0 <= grid[i][j] <= 50"
