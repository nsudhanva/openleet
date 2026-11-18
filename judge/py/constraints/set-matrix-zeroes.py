"""Set Matrix Zeroes: an m x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    assert isinstance(matrix, list) and matrix, "1 <= m"
    m = len(matrix)
    assert all(isinstance(r, list) for r in matrix), "matrix is a list of lists"
    n = len(matrix[0])
    assert 1 <= m <= 200 and 1 <= n <= 200, "1 <= m, n <= 200"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-(2**31) <= v <= 2**31 - 1 for r in matrix for v in r), (
        "-2^31 <= matrix[i][j] <= 2^31 - 1"
    )
