"""Maximum Matrix Sum: an n x n integer matrix."""


def check(matrix: list[list[int]]) -> None:
    n = len(matrix)
    assert 2 <= n <= 250, "2 <= n <= 250"
    assert all(len(row) == n for row in matrix), "n == matrix.length == matrix[i].length"
    assert all(-(10**5) <= v <= 10**5 for row in matrix for v in row), (
        "-10^5 <= matrix[i][j] <= 10^5"
    )
