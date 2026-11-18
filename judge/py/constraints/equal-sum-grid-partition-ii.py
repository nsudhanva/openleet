"""Equal Sum Grid Partition II: an m x n grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert all(isinstance(row, list) for row in grid), "grid is a list of rows"
    n = len(grid[0])
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert 2 <= m * n <= 10**5, "2 <= m * n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for row in grid for v in row), (
        "1 <= grid[i][j] <= 10^5"
    )
