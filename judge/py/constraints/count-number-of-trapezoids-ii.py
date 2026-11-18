"""Count Number of Trapezoids II: distinct 2D integer points."""


def check(points: list[list[int]]) -> None:
    assert 4 <= len(points) <= 500, "4 <= points.length <= 500"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-1000 <= v <= 1000 for p in points for v in p), "-1000 <= xi, yi <= 1000"
    assert len({(x, y) for x, y in points}) == len(points), "all points are pairwise distinct"
