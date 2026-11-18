"""Largest Triangle Area: a list of unique integer points."""


def check(points: list[list[int]]) -> None:
    assert 3 <= len(points) <= 50, "3 <= points.length <= 50"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-50 <= v <= 50 for p in points for v in p), "-50 <= xi, yi <= 50"
    assert len({tuple(p) for p in points}) == len(points), "all points are unique"
