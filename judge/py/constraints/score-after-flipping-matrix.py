"""Score After Flipping Matrix: an m x n binary grid."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 20, "1 <= m <= 20"
    n = len(grid[0])
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is either 0 or 1"
