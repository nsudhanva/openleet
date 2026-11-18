"""Smallest Rectangle Enclosing Black Pixels: a '0'/'1' grid with one black region and a black
pixel (x, y)."""


def check(image: list[list[str]], x: int, y: int) -> None:
    m = len(image)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(image[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in image), "n == image[i].length"
    assert all(c in ("0", "1") for r in image for c in r), "image[i][j] is either '0' or '1'"
    assert 0 <= x < m, "0 <= x < m"
    assert 0 <= y < n, "0 <= y < n"
    assert image[x][y] == "1", "image[x][y] == '1'"
    total = sum(c == "1" for r in image for c in r)
    seen = {(x, y)}
    stack = [(x, y)]
    while stack:
        i, j = stack.pop()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < m and 0 <= b < n and image[a][b] == "1" and (a, b) not in seen:
                seen.add((a, b))
                stack.append((a, b))
    assert len(seen) == total, "the black pixels form one component"
