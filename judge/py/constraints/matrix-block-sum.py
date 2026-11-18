"""Matrix Block Sum: an m x n matrix of 1..100 and a radius k."""


def check(mat: list[list[int]], k: int) -> None:
    m = len(mat)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(mat[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in mat), "n == mat[i].length"
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert all(1 <= v <= 100 for r in mat for v in r), "1 <= mat[i][j] <= 100"
