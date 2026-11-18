"""Rank Transform of a Matrix: an m x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(matrix[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-(10**9) <= v <= 10**9 for r in matrix for v in r), (
        "-10^9 <= matrix[row][col] <= 10^9"
    )
