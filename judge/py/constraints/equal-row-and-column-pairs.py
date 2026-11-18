"""Equal Row and Column Pairs: an n x n grid of positive integers."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(isinstance(row, list) and len(row) == n for row in grid), (
        "n == grid.length == grid[i].length"
    )
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for row in grid for v in row), (
        "1 <= grid[i][j] <= 10^5"
    )
