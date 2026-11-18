"""Maximum Non Negative Product in a Matrix: an m x n grid of small integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 15, "1 <= m <= 15"
    n = len(grid[0])
    assert 1 <= n <= 15, "1 <= n <= 15"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(-4 <= v <= 4 for row in grid for v in row), "-4 <= grid[i][j] <= 4"
