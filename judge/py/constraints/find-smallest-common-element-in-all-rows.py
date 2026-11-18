"""Find Smallest Common Element in All Rows: an m x n matrix with strictly increasing rows."""

from itertools import pairwise


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(mat[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(r) == n for r in mat), "n == mat[i].length"
    assert all(1 <= v <= 10**4 for r in mat for v in r), "1 <= mat[i][j] <= 10^4"
    assert all(a < b for r in mat for a, b in pairwise(r)), (
        "mat[i] is sorted in strictly increasing order"
    )
