"""Maximum Rows Covered by Columns: an m x n binary matrix and a column count."""


def check(matrix: list[list[int]], numSelect: int) -> None:
    m = len(matrix)
    assert 1 <= m <= 12, "1 <= m <= 12"
    n = len(matrix[0])
    assert 1 <= n <= 12, "1 <= n <= 12"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    assert all(v in (0, 1) for row in matrix for v in row), "matrix[i][j] is either 0 or 1"
    assert 1 <= numSelect <= n, "1 <= numSelect <= n"
