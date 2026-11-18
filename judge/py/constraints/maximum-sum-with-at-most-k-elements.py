"""Maximum Sum With at Most K Elements: an n x m grid, per-row limits and k."""


def check(grid: list[list[int]], limits: list[int], k: int) -> None:
    n = len(grid)
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert len(limits) == n, "n == grid.length == limits.length"
    m = len(grid[0])
    assert 1 <= m <= 500, "1 <= m <= 500"
    assert all(len(row) == m for row in grid), "m == grid[i].length"
    assert all(0 <= v <= 10**5 for row in grid for v in row), "0 <= grid[i][j] <= 10^5"
    assert all(0 <= x <= m for x in limits), "0 <= limits[i] <= m"
    assert 0 <= k <= min(n * m, sum(limits)), "0 <= k <= min(n * m, sum(limits))"
