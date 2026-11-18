"""Cyclically Shift Rows and Columns: an n x n grid with a shift amount per row and per column."""


def check(n: int, grid: list[list[int]], rowShift: list[int], colShift: list[int]) -> None:
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert len(grid) == n, "n == grid.length"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(1 <= v <= 100 for row in grid for v in row), "1 <= grid[i][j] <= 100"
    assert len(rowShift) == len(colShift) == n, "rowShift.length == colShift.length == n"
    assert all(0 <= v < n for v in rowShift + colShift), "0 <= rowShift[i], colShift[i] < n"
