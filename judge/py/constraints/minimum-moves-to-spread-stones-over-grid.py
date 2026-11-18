"""Minimum Moves to Spread Stones Over Grid: a 3 x 3 grid of stone counts summing to 9."""


def check(grid: list[list[int]]) -> None:
    assert len(grid) == 3, "grid.length == 3"
    assert all(len(r) == 3 for r in grid), "grid[i].length == 3"
    assert all(0 <= v <= 9 for r in grid for v in r), "0 <= grid[i][j] <= 9"
    assert sum(sum(r) for r in grid) == 9, "Sum of grid is equal to 9"
