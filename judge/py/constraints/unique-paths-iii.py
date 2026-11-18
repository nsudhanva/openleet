"""Unique Paths III: a small grid with one start (1), one end (2), empty (0) and obstacles (-1)."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 20, "1 <= m <= 20"
    assert all(isinstance(r, list) for r in grid), "grid[i] is a list"
    n = len(grid[0])
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert 1 <= m * n <= 20, "1 <= m * n <= 20"
    cells = [v for r in grid for v in r]
    assert all(v in (-1, 0, 1, 2) for v in cells), "-1 <= grid[i][j] <= 2"
    assert cells.count(1) == 1, "exactly one starting cell"
    assert cells.count(2) == 1, "exactly one ending cell"
