"""Find a Safe Walk Through a Grid: an m x n grid of 0/1 cells and a health value."""


def check(grid: list[list[int]], health: int) -> None:
    m = len(grid)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(grid[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert m * n >= 2, "2 <= m * n"
    assert 1 <= health <= m + n, "1 <= health <= m + n"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
