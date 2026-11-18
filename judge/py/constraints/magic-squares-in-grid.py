"""Magic Squares In Grid: a grid of integers 0..15."""


def check(grid: list[list[int]]) -> None:
    row = len(grid)
    assert 1 <= row <= 10, "1 <= row <= 10"
    col = len(grid[0])
    assert 1 <= col <= 10, "1 <= col <= 10"
    assert all(len(r) == col for r in grid), "col == grid[i].length"
    assert all(0 <= v <= 15 for r in grid for v in r), "0 <= grid[i][j] <= 15"
