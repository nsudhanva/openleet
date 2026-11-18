"""Count Square Submatrices with All Ones: a 0/1 matrix."""


def check(matrix: list[list[int]]) -> None:
    assert 1 <= len(matrix) <= 300, "1 <= arr.length <= 300"
    n = len(matrix[0])
    assert 1 <= n <= 300, "1 <= arr[0].length <= 300"
    assert all(len(row) == n for row in matrix), "matrix is rectangular"
    assert all(0 <= v <= 1 for row in matrix for v in row), "0 <= arr[i][j] <= 1"
