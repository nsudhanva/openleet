"""01 Matrix: a binary grid with at least one 0."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 10**4, "1 <= m <= 10^4"
    assert all(isinstance(r, list) for r in mat), "mat is a matrix"
    n = len(mat[0])
    assert all(len(r) == n for r in mat), "n == mat[i].length"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= m * n <= 10**4, "1 <= m * n <= 10^4"
    assert all(v in (0, 1) for r in mat for v in r), "mat[i][j] is either 0 or 1"
    assert any(v == 0 for r in mat for v in r), "There is at least one 0 in mat"
