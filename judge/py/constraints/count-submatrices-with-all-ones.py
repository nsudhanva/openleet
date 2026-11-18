"""Count Submatrices With All Ones: a binary matrix."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 150, "1 <= m <= 150"
    n = len(mat[0])
    assert 1 <= n <= 150, "1 <= n <= 150"
    assert all(len(r) == n for r in mat), "n == mat[i].length"
    assert all(v in (0, 1) for r in mat for v in r), "mat[i][j] is 0 or 1"
