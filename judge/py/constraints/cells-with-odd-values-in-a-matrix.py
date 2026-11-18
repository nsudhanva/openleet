"""Cells with Odd Values in a Matrix: matrix dimensions and [row, col] increments."""


def check(m: int, n: int, indices: list[list[int]]) -> None:
    assert 1 <= m <= 50 and 1 <= n <= 50, "1 <= m, n <= 50"
    assert isinstance(indices, list), "indices is a list"
    assert 1 <= len(indices) <= 100, "1 <= indices.length <= 100"
    assert all(isinstance(p, list) and len(p) == 2 for p in indices), "indices[i].length == 2"
    assert all(0 <= r < m for r, _ in indices), "0 <= ri < m"
    assert all(0 <= c < n for _, c in indices), "0 <= ci < n"
