"""Grid Game: a 2 x n grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    assert len(grid) == 2, "grid.length == 2"
    n = len(grid[0])
    assert len(grid[1]) == n, "n == grid[r].length"
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(1 <= v <= 10**5 for row in grid for v in row), "1 <= grid[r][c] <= 10^5"
