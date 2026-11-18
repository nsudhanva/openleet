"""Largest Submatrix With Rearrangements: a binary matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert m >= 1, "m >= 1"
    n = len(matrix[0])
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(v in (0, 1) for row in matrix for v in row), "matrix[i][j] is either 0 or 1"
