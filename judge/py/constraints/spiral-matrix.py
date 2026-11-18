"""Spiral Matrix: an m x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 10, "1 <= m <= 10"
    n = len(matrix[0])
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(isinstance(v, int) and -100 <= v <= 100 for r in matrix for v in r), (
        "-100 <= matrix[i][j] <= 100"
    )
