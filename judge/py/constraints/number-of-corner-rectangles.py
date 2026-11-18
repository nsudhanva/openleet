"""Number of Corner Rectangles: an m x n 0/1 grid with 1 to 6000 ones."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(grid[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    ones = sum(sum(row) for row in grid)
    assert 1 <= ones <= 6000, "the number of 1's in the grid is in the range [1, 6000]"
