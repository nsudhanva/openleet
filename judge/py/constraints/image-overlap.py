"""Image Overlap: two n x n binary images."""


def check(img1: list[list[int]], img2: list[list[int]]) -> None:
    n = len(img1)
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert all(len(r) == n for r in img1), "n == img1.length == img1[i].length"
    assert len(img2) == n and all(len(r) == n for r in img2), "n == img2.length == img2[i].length"
    assert all(v in (0, 1) for r in img1 for v in r), "img1[i][j] is either 0 or 1"
    assert all(v in (0, 1) for r in img2 for v in r), "img2[i][j] is either 0 or 1"
