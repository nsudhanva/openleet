"""Find the Minimum Area to Cover All Ones I: a 0/1 grid with at least one 1."""


def check(grid: list[list[int]]) -> None:
    assert 1 <= len(grid) <= 1000, "1 <= grid.length <= 1000"
    assert all(1 <= len(row) <= 1000 for row in grid), "1 <= grid[i].length <= 1000"
    assert all(len(row) == len(grid[0]) for row in grid), "grid is rectangular"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert any(1 in row for row in grid), "at least one 1 in grid"
