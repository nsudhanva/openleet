"""Image Smoother: an m x n grayscale image."""


def check(img: list[list[int]]) -> None:
    m = len(img)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(img[0])
    assert all(len(r) == n for r in img), "n == img[i].length"
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(0 <= v <= 255 for r in img for v in r), "0 <= img[i][j] <= 255"
