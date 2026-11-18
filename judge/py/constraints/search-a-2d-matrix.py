"""Search a 2D Matrix: an m x n integer matrix, rows sorted, each row starting above the last
row's end, plus a target."""


def check(matrix: list[list[int]], target: int) -> None:
    assert isinstance(matrix, list) and matrix, "1 <= m"
    m = len(matrix)
    assert all(isinstance(r, list) for r in matrix), "matrix is a list of lists"
    n = len(matrix[0])
    assert 1 <= m <= 100 and 1 <= n <= 100, "1 <= m, n <= 100"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-(10**4) <= v <= 10**4 for r in matrix for v in r), "-10^4 <= matrix[i][j] <= 10^4"
    assert -(10**4) <= target <= 10**4, "-10^4 <= target <= 10^4"
    assert all(r[j] <= r[j + 1] for r in matrix for j in range(n - 1)), "each row is non-decreasing"
    assert all(matrix[i][0] > matrix[i - 1][-1] for i in range(1, m)), (
        "first integer of each row > last integer of the previous row"
    )
