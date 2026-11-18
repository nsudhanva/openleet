"""Minimum Cost Path with Teleportations: a grid of costs and a teleport count k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 2 <= m <= 80, "2 <= m <= 80"
    n = len(grid[0])
    assert 2 <= n <= 80, "2 <= n <= 80"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(0 <= v <= 10**4 for row in grid for v in row), "0 <= grid[i][j] <= 10^4"
    assert 0 <= k <= 10, "0 <= k <= 10"
