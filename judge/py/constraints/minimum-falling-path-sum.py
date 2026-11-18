"""Minimum Falling Path Sum: an n x n integer grid."""


def check(matrix: list[list[int]]) -> None:
    n = len(matrix)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in matrix), "n == matrix.length == matrix[i].length"
    assert all(-100 <= x <= 100 for row in matrix for x in row), "-100 <= matrix[i][j] <= 100"
