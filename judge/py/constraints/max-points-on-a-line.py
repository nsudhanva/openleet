"""Max Points on a Line: distinct points in the plane."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 300, "1 <= points.length <= 300"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**4) <= c <= 10**4 for p in points for c in p), "-10^4 <= xi, yi <= 10^4"
    assert len({tuple(p) for p in points}) == len(points), "all the points are unique"
