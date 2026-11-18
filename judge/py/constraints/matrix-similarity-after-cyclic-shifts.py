"""Matrix Similarity After Cyclic Shifts: an integer matrix and a shift count."""


def check(mat: list[list[int]], k: int) -> None:
    assert 1 <= len(mat) <= 25, "1 <= mat.length <= 25"
    assert all(1 <= len(row) <= 25 for row in mat), "1 <= mat[i].length <= 25"
    assert all(1 <= v <= 25 for row in mat for v in row), "1 <= mat[i][j] <= 25"
    assert 1 <= k <= 50, "1 <= k <= 50"
