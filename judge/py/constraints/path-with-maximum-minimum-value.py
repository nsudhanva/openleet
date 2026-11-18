"""Path With Maximum Minimum Value: a grid of integers."""


def check(grid: list[list[int]]) -> None:
    assert isinstance(grid, list) and grid, "grid is a non-empty matrix"
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0]) if isinstance(grid[0], list) else 0
    assert all(isinstance(r, list) and len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(isinstance(v, int) and 0 <= v <= 10**9 for r in grid for v in r), (
        "0 <= grid[i][j] <= 10^9"
    )
