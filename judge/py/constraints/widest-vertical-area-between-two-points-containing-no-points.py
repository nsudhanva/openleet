"""Widest Vertical Area Between Two Points Containing No Points: a list of [x, y] points."""


def check(points: list[list[int]]) -> None:
    n = len(points)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= v <= 10**9 for p in points for v in p), "0 <= xi, yi <= 10^9"
