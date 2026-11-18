"""Flip Columns For Maximum Number of Equal Rows: an m x n binary matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(matrix[0])
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert all(v in (0, 1) for row in matrix for v in row), "matrix[i][j] is either 0 or 1"
