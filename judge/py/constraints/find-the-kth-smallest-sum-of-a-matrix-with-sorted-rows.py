"""Find the Kth Smallest Sum of a Matrix With Sorted Rows: sorted-row matrix and k."""


def check(mat: list[list[int]], k: int) -> None:
    m = len(mat)
    assert 1 <= m <= 40, "1 <= m <= 40"
    n = len(mat[0])
    assert 1 <= n <= 40, "1 <= n <= 40"
    assert all(len(row) == n for row in mat), "n == mat[i].length"
    assert all(1 <= v <= 5000 for row in mat for v in row), "1 <= mat[i][j] <= 5000"
    assert 1 <= k <= min(200, n**m), "1 <= k <= min(200, n^m)"
    assert all(row[i] <= row[i + 1] for row in mat for i in range(n - 1)), (
        "mat[i] is a non-decreasing array"
    )
