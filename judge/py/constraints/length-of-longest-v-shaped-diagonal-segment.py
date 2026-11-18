"""Length of Longest V-Shaped Diagonal Segment: an n x m grid of 0, 1 and 2."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 1 <= n <= 500, "1 <= n <= 500"
    m = len(grid[0])
    assert 1 <= m <= 500, "1 <= m <= 500"
    assert all(len(row) == m for row in grid), "m == grid[i].length"
    assert all(v in (0, 1, 2) for row in grid for v in row), "grid[i][j] is either 0, 1 or 2"
