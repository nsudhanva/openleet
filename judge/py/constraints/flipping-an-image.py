"""Flipping an Image: an n x n binary matrix."""


def check(image: list[list[int]]) -> None:
    n = len(image)
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(row) == n for row in image), "n == image.length == image[i].length"
    assert all(v in (0, 1) for row in image for v in row), "image[i][j] is 0 or 1"
