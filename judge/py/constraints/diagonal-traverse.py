"""Diagonal Traverse: an m x n integer matrix."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 10**4, "1 <= m <= 10^4"
    n = len(mat[0])
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert 1 <= m * n <= 10**4, "1 <= m * n <= 10^4"
    assert all(-(10**5) <= v <= 10**5 for row in mat for v in row), "-10^5 <= mat[i][j] <= 10^5"
