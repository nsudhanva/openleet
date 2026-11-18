"""Maximal Rectangle: a matrix of '0' and '1' characters."""


def check(matrix: list[list[str]]) -> None:
    rows = len(matrix)
    assert 1 <= rows <= 200, "1 <= rows <= 200"
    assert matrix, "non-empty"
    cols = len(matrix[0])
    assert 1 <= cols <= 200, "1 <= cols <= 200"
    assert all(len(row) == cols for row in matrix), "cols == matrix[i].length"
    assert all(v in ("0", "1") for row in matrix for v in row), "matrix[i][j] is '0' or '1'"
