"""Maximum Side Length of a Square with Sum Less than or Equal to Threshold: an m x n matrix
of non-negative integers and a threshold."""


def check(mat: list[list[int]], threshold: int) -> None:
    m = len(mat)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(mat[0])
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(0 <= v <= 10**4 for row in mat for v in row), "0 <= mat[i][j] <= 10^4"
    assert 0 <= threshold <= 10**5, "0 <= threshold <= 10^5"
