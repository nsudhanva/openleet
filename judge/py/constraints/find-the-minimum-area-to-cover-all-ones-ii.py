"""Find the Minimum Area to Cover All Ones II: a 0/1 grid with at least three 1's."""


def check(grid: list[list[int]]) -> None:
    assert 1 <= len(grid) <= 30, "1 <= grid.length <= 30"
    assert all(1 <= len(row) <= 30 for row in grid), "1 <= grid[i].length <= 30"
    assert all(len(row) == len(grid[0]) for row in grid), "grid is rectangular"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert sum(sum(row) for row in grid) >= 3, "at least three 1's in grid"
