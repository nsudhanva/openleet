"""The K Weakest Rows in a Matrix: an m x n binary matrix and k."""


def check(mat: list[list[int]], k: int) -> None:
    m = len(mat)
    assert 2 <= m <= 100, "2 <= m <= 100"
    n = len(mat[0])
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert 1 <= k <= m, "1 <= k <= m"
    assert all(v in (0, 1) for row in mat for v in row), "mat[i][j] is either 0 or 1"
    assert all(row == sorted(row, reverse=True) for row in mat), (
        "all the 1's appear to the left of all the 0's in each row"
    )
