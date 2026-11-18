"""Lonely Pixel II: an m x n picture of 'W' and 'B' and a target count."""


def check(picture: list[list[str]], target: int) -> None:
    m = len(picture)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(picture[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in picture), "n == picture[i].length"
    assert all(c in ("W", "B") for row in picture for c in row), "picture[i][j] is 'W' or 'B'"
    assert 1 <= target <= min(m, n), "1 <= target <= min(m, n)"
