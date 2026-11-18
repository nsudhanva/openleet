"""Sort the Matrix Diagonally: an m x n grid of small positive integers."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(mat[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(isinstance(v, int) and 1 <= v <= 100 for row in mat for v in row), (
        "1 <= mat[i][j] <= 100"
    )
