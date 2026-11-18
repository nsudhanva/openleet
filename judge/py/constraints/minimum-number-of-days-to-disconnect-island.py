"""Minimum Number of Days to Disconnect Island: a binary grid of land and water."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 30, "1 <= m <= 30"
    n = len(grid[0])
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is either 0 or 1"
