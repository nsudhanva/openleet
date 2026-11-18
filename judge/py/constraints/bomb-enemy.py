"""Bomb Enemy: a grid of 'W' walls, 'E' enemies and '0' empty cells."""


def check(grid: list[list[str]]) -> None:
    m = len(grid)
    assert 1 <= m <= 500, "1 <= m <= 500"
    assert all(isinstance(row, list) for row in grid), "grid is a list of rows"
    n = len(grid[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(c in ("W", "E", "0") for row in grid for c in row), (
        "grid[i][j] is either 'W', 'E', or '0'"
    )
