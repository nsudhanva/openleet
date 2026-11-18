"""Find a Peak Element II: an m x n matrix where no two adjacent cells are equal."""


def check(mat: list[list[int]]) -> None:
    m = len(mat)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(mat[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(1 <= v <= 10**5 for row in mat for v in row), "1 <= mat[i][j] <= 10^5"
    for i in range(m):
        row = mat[i]
        assert all(row[j] != row[j + 1] for j in range(n - 1)), "no two adjacent cells are equal"
        if i + 1 < m:
            below = mat[i + 1]
            assert all(row[j] != below[j] for j in range(n)), "no two adjacent cells are equal"
