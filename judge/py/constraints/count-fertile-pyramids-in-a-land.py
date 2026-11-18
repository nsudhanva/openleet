"""Count Fertile Pyramids in a Land: a 0/1 grid with m * n <= 10^5."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is 0 or 1"
