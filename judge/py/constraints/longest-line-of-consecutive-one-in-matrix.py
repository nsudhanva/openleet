"""Longest Line of Consecutive One in Matrix: an m x n binary grid."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 10**4, "1 <= m <= 10^4"
    n = len(mat[0])
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert 1 <= m * n <= 10**4, "1 <= m * n <= 10^4"
    assert all(v in (0, 1) for row in mat for v in row), "mat[i][j] is either 0 or 1"
