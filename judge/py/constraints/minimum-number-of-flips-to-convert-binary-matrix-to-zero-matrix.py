"""Minimum Number of Flips to Convert Binary Matrix to Zero Matrix: an m x n binary matrix."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 3, "1 <= m <= 3"
    n = len(mat[0])
    assert 1 <= n <= 3, "1 <= n <= 3"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(v in (0, 1) for row in mat for v in row), "mat[i][j] is either 0 or 1"
