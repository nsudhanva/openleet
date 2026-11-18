"""Maximum Number of Points From Grid Queries: an m x n matrix and a list of queries."""


def check(grid: list[list[int]], queries: list[int]) -> None:
    m = len(grid)
    assert 2 <= m <= 1000, "2 <= m <= 1000"
    n = len(grid[0])
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 4 <= m * n <= 10**5, "4 <= m * n <= 10^5"
    assert 1 <= len(queries) <= 10**4, "1 <= k <= 10^4"
    assert all(1 <= v <= 10**6 for row in grid for v in row), "1 <= grid[i][j] <= 10^6"
    assert all(1 <= q <= 10**6 for q in queries), "1 <= queries[i] <= 10^6"
