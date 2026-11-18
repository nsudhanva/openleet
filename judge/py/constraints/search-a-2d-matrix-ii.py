"""Search a 2D Matrix II: an m x n integer matrix with sorted rows and columns, plus a
target."""


def check(matrix: list[list[int]], target: int) -> None:
    assert isinstance(matrix, list) and matrix, "1 <= m"
    m = len(matrix)
    assert all(isinstance(r, list) for r in matrix), "matrix is a list of lists"
    n = len(matrix[0])
    assert 1 <= m <= 300 and 1 <= n <= 300, "1 <= n, m <= 300"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-(10**9) <= v <= 10**9 for r in matrix for v in r), "-10^9 <= matrix[i][j] <= 10^9"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
    assert all(r[j] <= r[j + 1] for r in matrix for j in range(n - 1)), "rows sorted ascending"
    assert all(matrix[i][j] <= matrix[i + 1][j] for i in range(m - 1) for j in range(n)), (
        "columns sorted ascending"
    )
