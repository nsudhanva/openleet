"""Toeplitz Matrix: an m x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 20, "1 <= m <= 20"
    n = len(matrix[0])
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(0 <= v <= 99 for row in matrix for v in row), "0 <= matrix[i][j] <= 99"
