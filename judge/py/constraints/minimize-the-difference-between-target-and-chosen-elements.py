"""Minimize the Difference Between Target and Chosen Elements: an m x n matrix and a target."""


def check(mat: list[list[int]], target: int) -> None:
    m = len(mat)
    assert 1 <= m <= 70, "1 <= m <= 70"
    n = len(mat[0])
    assert 1 <= n <= 70, "1 <= n <= 70"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(1 <= v <= 70 for row in mat for v in row), "1 <= mat[i][j] <= 70"
    assert 1 <= target <= 800, "1 <= target <= 800"
