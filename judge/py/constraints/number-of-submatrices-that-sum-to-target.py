"""Number of Submatrices That Sum to Target: an integer matrix and a target."""


def check(matrix: list[list[int]], target: int) -> None:
    assert isinstance(matrix, list), "matrix is a list"
    assert 1 <= len(matrix) <= 100, "1 <= matrix.length <= 100"
    assert all(isinstance(r, list) for r in matrix), "matrix[i] is a list"
    assert 1 <= len(matrix[0]) <= 100, "1 <= matrix[0].length <= 100"
    assert all(len(r) == len(matrix[0]) for r in matrix), "matrix is rectangular"
    assert all(-1000 <= v <= 1000 for r in matrix for v in r), "-1000 <= matrix[i][j] <= 1000"
    assert -(10**8) <= target <= 10**8, "-10^8 <= target <= 10^8"
