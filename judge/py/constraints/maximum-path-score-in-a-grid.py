"""Maximum Path Score in a Grid: an m x n grid of 0/1/2 cells and a cost budget k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(grid[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 0 <= k <= 10**3, "0 <= k <= 10^3"
    assert grid[0][0] == 0, "grid[0][0] == 0"
    assert all(0 <= v <= 2 for row in grid for v in row), "0 <= grid[i][j] <= 2"
