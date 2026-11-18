"""Count Islands With Total Value Divisible by K: a grid of non-negative values and k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(0 <= v <= 10**6 for r in grid for v in r), "0 <= grid[i][j] <= 10^6"
    assert 1 <= k <= 10**6, "1 <= k <= 10^6"
