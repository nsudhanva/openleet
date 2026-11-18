"""Flood Fill: an m x n grid of colors, a start cell and a new color."""


def check(image: list[list[int]], sr: int, sc: int, color: int) -> None:
    m = len(image)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(image[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in image), "n == image[i].length"
    assert all(0 <= v < 2**16 for row in image for v in row), "0 <= image[i][j] < 2^16"
    assert 0 <= color < 2**16, "0 <= color < 2^16"
    assert 0 <= sr < m, "0 <= sr < m"
    assert 0 <= sc < n, "0 <= sc < n"
