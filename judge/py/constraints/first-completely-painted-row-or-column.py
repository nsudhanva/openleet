"""First Completely Painted Row or Column: a painting order and an m x n matrix, both
permutations of 1..m*n."""


def check(arr: list[int], mat: list[list[int]]) -> None:
    m = len(mat)
    assert m >= 1, "1 <= m"
    n = len(mat[0])
    assert all(len(row) == n for row in mat), "n = mat[i].length"
    assert 1 <= m <= 10**5 and 1 <= n <= 10**5, "1 <= m, n <= 10^5"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert len(arr) == m * n, "arr.length == m * n"
    full = set(range(1, m * n + 1))
    assert set(arr) == full and len(set(arr)) == len(arr), "arr holds each of 1..m*n once"
    flat = [v for row in mat for v in row]
    assert set(flat) == full and len(set(flat)) == len(flat), "mat holds each of 1..m*n once"
