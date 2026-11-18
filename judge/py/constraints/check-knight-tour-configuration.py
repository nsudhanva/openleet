"""Check Knight Tour Configuration: an n x n grid of unique integers in [0, n*n)."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 3 <= n <= 7, "3 <= n <= 7"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    values = [v for row in grid for v in row]
    assert all(0 <= v < n * n for v in values), "0 <= grid[row][col] < n * n"
    assert len(set(values)) == len(values), "All integers in grid are unique"
