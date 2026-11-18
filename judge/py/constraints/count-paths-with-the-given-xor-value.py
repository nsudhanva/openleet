"""Count Paths With the Given XOR Value: a grid of values below 16 and k."""


def check(grid: list[list[int]], k: int) -> None:
    m = len(grid)
    assert 1 <= m <= 300, "1 <= m == grid.length <= 300"
    n = len(grid[0])
    assert 1 <= n <= 300, "1 <= n == grid[r].length <= 300"
    assert all(len(row) == n for row in grid), "n == grid[r].length"
    assert all(0 <= v < 16 for row in grid for v in row), "0 <= grid[r][c] < 16"
    assert 0 <= k < 16, "0 <= k < 16"
