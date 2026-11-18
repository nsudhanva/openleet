"""Longest Increasing Path in a Matrix: an m x n grid of non-negative ints."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(matrix[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert all(0 <= v <= 2**31 - 1 for row in matrix for v in row), "0 <= matrix[i][j] <= 2^31 - 1"
