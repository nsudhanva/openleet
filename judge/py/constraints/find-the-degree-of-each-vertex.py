"""Find the Degree of Each Vertex: an n x n symmetric 0/1 adjacency matrix with zero diagonal."""


def check(matrix: list[list[int]]) -> None:
    n = len(matrix)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(row) == n for row in matrix), "n == matrix.length == matrix[i].length"
    assert all(v in (0, 1) for row in matrix for v in row), "matrix[i][j] is either 0 or 1"
    assert all(matrix[i][i] == 0 for i in range(n)), "matrix[i][i] == 0"
    assert all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(i)), (
        "matrix[i][j] == matrix[j][i]"
    )
