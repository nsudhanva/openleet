"""Convex Polygon: a list of unique [x, y] points forming a polygon."""


def check(points: list[list[int]]) -> None:
    assert isinstance(points, list), "points is a list"
    assert 3 <= len(points) <= 10**4, "3 <= points.length <= 10^4"
    assert all(isinstance(p, list) and len(p) == 2 for p in points), "points[i].length == 2"
    assert all(isinstance(c, int) for p in points for c in p), "xi, yi are integers"
    assert all(-(10**4) <= c <= 10**4 for p in points for c in p), "-10^4 <= xi, yi <= 10^4"
    assert len({(p[0], p[1]) for p in points}) == len(points), "All the given points are unique"
