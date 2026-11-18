"""Rotate Image: an n x n matrix."""


def check(matrix: list[list[int]]) -> None:
    n = len(matrix)
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(r) == n for r in matrix), "n == matrix.length == matrix[i].length"
    assert all(-1000 <= v <= 1000 for r in matrix for v in r), "-1000 <= matrix[i][j] <= 1000"
