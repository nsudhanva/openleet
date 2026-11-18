"""Check if Matrix Is X-Matrix: an n x n integer grid."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 3 <= n <= 100, "3 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(0 <= v <= 10**5 for row in grid for v in row), "0 <= grid[i][j] <= 10^5"
