"""Making A Large Island: an n x n binary grid."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(r) == n for r in grid), "n == grid.length == grid[i].length"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is 0 or 1"
