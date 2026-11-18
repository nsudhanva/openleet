"""Find the Grid of Region Average: an m x n grayscale image and a threshold."""


def check(image: list[list[int]], threshold: int) -> None:
    m = len(image)
    assert 3 <= m <= 500, "3 <= m <= 500"
    n = len(image[0])
    assert 3 <= n <= 500, "3 <= n <= 500"
    assert all(len(row) == n for row in image), "image is an m x n grid"
    assert all(0 <= v <= 255 for row in image for v in row), "0 <= image[i][j] <= 255"
    assert 0 <= threshold <= 255, "0 <= threshold <= 255"
