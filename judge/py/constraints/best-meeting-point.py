"""Best Meeting Point: an m x n binary grid with friends' homes marked 1."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(grid[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert sum(sum(row) for row in grid) >= 2, "at least two friends in the grid"
