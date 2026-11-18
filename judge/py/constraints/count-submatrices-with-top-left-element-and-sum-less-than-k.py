"""Count Submatrices with Top-Left Element and Sum Less Than k: an integer grid and k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(grid[0])
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(0 <= v <= 1000 for r in grid for v in r), "0 <= grid[i][j] <= 1000"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
