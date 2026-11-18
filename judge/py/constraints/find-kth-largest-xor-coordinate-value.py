"""Find Kth Largest XOR Coordinate Value: an m x n matrix of non-negative integers and a rank
k."""


def check(matrix: list[list[int]], k: int) -> None:
    m = len(matrix)
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    n = len(matrix[0]) if m else 0
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert all(0 <= v <= 10**6 for row in matrix for v in row), "0 <= matrix[i][j] <= 10^6"
    assert 1 <= k <= m * n, "1 <= k <= m * n"
