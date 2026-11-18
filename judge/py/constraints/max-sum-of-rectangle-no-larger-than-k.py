"""Max Sum of Rectangle No Larger Than K: an m x n integer matrix and a bound."""


def check(matrix: list[list[int]], k: int) -> None:
    m = len(matrix)
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert matrix, "non-empty"
    n = len(matrix[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert all(-100 <= v <= 100 for row in matrix for v in row), "-100 <= matrix[i][j] <= 100"
    assert -(10**5) <= k <= 10**5, "-10^5 <= k <= 10^5"
