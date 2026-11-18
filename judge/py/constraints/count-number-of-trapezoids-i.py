"""Count Number of Trapezoids I: distinct 2D integer points."""


def check(points: list[list[int]]) -> None:
    assert 4 <= len(points) <= 10**5, "4 <= points.length <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**8) <= v <= 10**8 for p in points for v in p), "-10^8 <= xi, yi <= 10^8"
    assert len({(x, y) for x, y in points}) == len(points), "all points are pairwise distinct"
