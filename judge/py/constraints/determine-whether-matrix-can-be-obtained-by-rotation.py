"""Determine Whether Matrix Can Be Obtained By Rotation: two n x n binary matrices."""


def check(mat: list[list[int]], target: list[list[int]]) -> None:
    n = len(mat)
    assert n == len(target), "n == mat.length == target.length"
    assert 1 <= n <= 10, "1 <= n <= 10"
    for m in (mat, target):
        assert all(len(row) == n for row in m), "n == mat[i].length == target[i].length"
        assert all(v in (0, 1) for row in m for v in row), "values are either 0 or 1"
