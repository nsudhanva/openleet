"""Maximum Area of Two Non-Overlapping Square Submatrices: an m x n binary matrix."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(mat[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in mat), "mat[i].length == n"
    assert all(v in (0, 1) for row in mat for v in row), "mat[i][j] is either 0 or 1"
