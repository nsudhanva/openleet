"""Kth Smallest Element in a Sorted Matrix: an n x n matrix sorted along rows and columns, and k."""

from itertools import pairwise


def check(matrix: list[list[int]], k: int) -> None:
    n = len(matrix)
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(len(r) == n for r in matrix), "n == matrix.length == matrix[i].length"
    assert all(-(10**9) <= v <= 10**9 for r in matrix for v in r), "-10^9 <= matrix[i][j] <= 10^9"
    assert all(a <= b for r in matrix for a, b in pairwise(r)), (
        "rows are sorted in non-decreasing order"
    )
    assert all(matrix[i][j] <= matrix[i + 1][j] for i in range(n - 1) for j in range(n)), (
        "columns are sorted in non-decreasing order"
    )
    assert 1 <= k <= n * n, "1 <= k <= n^2"
