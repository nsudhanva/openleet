"""Count Submatrices With Equal Frequency of X and Y: a grid of 'X', 'Y' and '.'."""


def check(grid: list[list[str]]) -> None:
    assert 1 <= len(grid) <= 1000, "1 <= grid.length <= 1000"
    n = len(grid[0])
    assert 1 <= n <= 1000, "1 <= grid[i].length <= 1000"
    assert all(len(r) == n for r in grid), "grid is rectangular"
    assert all(v in ("X", "Y", ".") for r in grid for v in r), "grid[i][j] is 'X', 'Y' or '.'"
