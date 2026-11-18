"""Find the Safest Path in a Grid: an n x n grid of 0 (empty) and 1 (thief)."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 400, "1 <= grid.length == n <= 400"
    assert all(len(row) == n for row in grid), "grid[i].length == n"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert any(v == 1 for row in grid for v in row), "there is at least one thief in the grid"
