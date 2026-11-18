"""Lucky Numbers in a Matrix: an m x n matrix of distinct positive integers."""


def check(matrix: list[list[int]]) -> None:
    m = len(matrix)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(matrix[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in matrix), "n == matrix[i].length"
    values = [v for row in matrix for v in row]
    assert all(1 <= v <= 10**5 for v in values), "1 <= matrix[i][j] <= 10^5"
    assert len(set(values)) == len(values), "all elements are distinct"
