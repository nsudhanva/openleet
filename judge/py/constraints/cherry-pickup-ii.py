"""Cherry Pickup II: a rows x cols grid of cherry counts."""


def check(grid: list[list[int]]) -> None:
    rows = len(grid)
    assert 2 <= rows <= 70, "2 <= rows <= 70"
    assert rows >= 1, "grid is not empty"
    cols = len(grid[0])
    assert all(len(r) == cols for r in grid), "cols == grid[i].length"
    assert 2 <= cols <= 70, "2 <= cols <= 70"
    assert all(0 <= v <= 100 for r in grid for v in r), "0 <= grid[i][j] <= 100"
