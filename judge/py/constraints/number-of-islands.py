"""Number of Islands: a rectangular grid of '0' and '1' characters."""


def check(grid: list[list[str]]) -> None:
    m = len(grid)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(c in ("0", "1") for row in grid for c in row), "grid[i][j] is '0' or '1'"
