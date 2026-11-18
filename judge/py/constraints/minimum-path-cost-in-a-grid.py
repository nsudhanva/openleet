"""Minimum Path Cost in a Grid: an m x n grid of distinct 0..m*n-1 and a move-cost table."""


def check(grid: list[list[int]], moveCost: list[list[int]]) -> None:
    m = len(grid)
    assert 2 <= m <= 50, "2 <= m <= 50"
    n = len(grid[0])
    assert 2 <= n <= 50, "2 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    values = [v for row in grid for v in row]
    assert sorted(values) == list(range(m * n)), (
        "grid consists of distinct integers from 0 to m * n - 1"
    )
    assert len(moveCost) == m * n, "moveCost.length == m * n"
    assert all(len(row) == n for row in moveCost), "moveCost[i].length == n"
    assert all(1 <= c <= 100 for row in moveCost for c in row), "1 <= moveCost[i][j] <= 100"
