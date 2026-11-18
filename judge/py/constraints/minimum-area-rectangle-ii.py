"""Minimum Area Rectangle II: distinct integer points in the plane."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 50, "1 <= points.length <= 50"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= v <= 4 * 10**4 for p in points for v in p), "0 <= xi, yi <= 4 * 10^4"
    assert len({tuple(p) for p in points}) == len(points), "all the given points are unique"
