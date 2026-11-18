"""Minimum Operations to Make a Uni-Value Grid: an m x n grid of positive integers and x."""


def check(grid: list[list[int]], x: int) -> None:
    assert isinstance(grid, list) and grid, "grid is a non-empty list"
    m = len(grid)
    assert all(isinstance(r, list) for r in grid), "grid rows are lists"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= m <= 10**5 and 1 <= n <= 10**5, "1 <= m, n <= 10^5"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert 1 <= x <= 10**4, "1 <= x <= 10^4"
    assert all(1 <= v <= 10**4 for r in grid for v in r), "1 <= grid[i][j] <= 10^4"
