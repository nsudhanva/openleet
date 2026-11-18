"""Matrix Diagonal Sum: a square integer matrix."""


def check(mat: list[list[int]]) -> None:
    n = len(mat)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in mat), "n == mat.length == mat[i].length"
    assert all(1 <= v <= 100 for row in mat for v in row), "1 <= mat[i][j] <= 100"
