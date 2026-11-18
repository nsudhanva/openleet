"""Sparse Matrix Multiplication: two integer matrices, m x k and k x n."""


def check(mat1: list[list[int]], mat2: list[list[int]]) -> None:
    m, k = len(mat1), len(mat2)
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert all(len(r) == k for r in mat1), "k == mat1[i].length == mat2.length"
    n = len(mat2[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in mat2), "n == mat2[i].length"
    assert all(isinstance(v, int) and -100 <= v <= 100 for r in mat1 for v in r), (
        "-100 <= mat1[i][j] <= 100"
    )
    assert all(isinstance(v, int) and -100 <= v <= 100 for r in mat2 for v in r), (
        "-100 <= mat2[i][j] <= 100"
    )
