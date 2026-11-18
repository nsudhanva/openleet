"""Number of Boomerangs: unique 2D points."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 500, "1 <= n <= 500"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**4) <= v <= 10**4 for p in points for v in p), "-10^4 <= xi, yi <= 10^4"
    assert len({(p[0], p[1]) for p in points}) == len(points), "all the points are unique"
