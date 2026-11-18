"""Sort Matrix by Diagonals: an n x n integer grid."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert all(len(row) == n for row in grid), "grid.length == grid[i].length == n"
    assert all(isinstance(v, int) and -(10**5) <= v <= 10**5 for row in grid for v in row), (
        "-10^5 <= grid[i][j] <= 10^5"
    )
