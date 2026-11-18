"""Shortest Distance from All Buildings: a grid of 0 (land), 1 (building), 2 (obstacle)."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1, 2) for row in grid for v in row), "grid[i][j] is either 0, 1, or 2"
    assert any(v == 1 for row in grid for v in row), (
        "There will be at least one building in the grid"
    )
