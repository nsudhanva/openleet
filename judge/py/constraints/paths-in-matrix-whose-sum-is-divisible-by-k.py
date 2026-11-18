"""Paths in Matrix Whose Sum Is Divisible by K: a grid of integers and k."""


def check(grid: list[list[int]], k: int) -> None:
    assert isinstance(grid, list) and grid, "grid is a non-empty matrix"
    m = len(grid)
    n = len(grid[0]) if isinstance(grid[0], list) else 0
    assert all(isinstance(r, list) and len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= m <= 5 * 10**4 and 1 <= n <= 5 * 10**4, "1 <= m, n <= 5 * 10^4"
    assert 1 <= m * n <= 5 * 10**4, "1 <= m * n <= 5 * 10^4"
    assert all(isinstance(v, int) and 0 <= v <= 100 for r in grid for v in r), (
        "0 <= grid[i][j] <= 100"
    )
    assert isinstance(k, int) and 1 <= k <= 50, "1 <= k <= 50"
