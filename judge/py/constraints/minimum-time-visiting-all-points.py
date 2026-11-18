"""Minimum Time Visiting All Points: a list of integer [x, y] points."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 100, "1 <= n <= 100"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-1000 <= c <= 1000 for p in points for c in p), "-1000 <= points[i][j] <= 1000"
