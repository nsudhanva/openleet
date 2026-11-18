"""Most Frequent Prime: an m x n matrix of digits 1..9."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 6, "1 <= m <= 6"
    assert mat and isinstance(mat[0], list), "mat is a non-empty matrix"
    n = len(mat[0])
    assert 1 <= n <= 6, "1 <= n <= 6"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(1 <= v <= 9 for row in mat for v in row), "1 <= mat[i][j] <= 9"
