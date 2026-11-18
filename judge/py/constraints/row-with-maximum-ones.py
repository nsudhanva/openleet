"""Row With Maximum Ones: an m x n binary matrix."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(mat[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in mat), "n == mat[i].length"
    assert all(v in (0, 1) for r in mat for v in r), "mat[i][j] is either 0 or 1"
