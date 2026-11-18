"""Reshape the Matrix: an m x n integer matrix and target dimensions r, c."""


def check(mat: list[list[int]], r: int, c: int) -> None:
    m = len(mat)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(mat[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(-1000 <= v <= 1000 for row in mat for v in row), "-1000 <= mat[i][j] <= 1000"
    assert 1 <= r <= 300, "1 <= r <= 300"
    assert 1 <= c <= 300, "1 <= c <= 300"
