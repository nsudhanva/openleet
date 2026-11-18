"""Lonely Pixel I: an m x n picture of 'W' and 'B'."""


def check(picture: list[list[str]]) -> None:
    m = len(picture)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(picture[0])
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(len(row) == n for row in picture), "n == picture[i].length"
    assert all(c in ("W", "B") for row in picture for c in row), "picture[i][j] is 'W' or 'B'"
