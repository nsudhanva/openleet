"""Transpose Matrix: an m x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(matrix[0])
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for r in matrix for v in r), "-10^9 <= matrix[i][j] <= 10^9"
