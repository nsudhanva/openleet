"""Path with Maximum Gold: a grid of gold amounts."""


def check(grid: list[list[int]]) -> None:
    assert isinstance(grid, list) and grid, "grid is a non-empty matrix"
    m = len(grid)
    assert 1 <= m <= 15, "1 <= m <= 15"
    n = len(grid[0]) if isinstance(grid[0], list) else 0
    assert all(isinstance(r, list) and len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= n <= 15, "1 <= n <= 15"
    vals = [v for r in grid for v in r]
    assert all(isinstance(v, int) and 0 <= v <= 100 for v in vals), "0 <= grid[i][j] <= 100"
    assert sum(v > 0 for v in vals) <= 25, "There are at most 25 cells containing gold"
