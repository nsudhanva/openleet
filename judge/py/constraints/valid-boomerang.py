"""Valid Boomerang: three 2D points."""


def check(points: list[list[int]]) -> None:
    assert isinstance(points, list) and len(points) == 3, "points.length == 3"
    assert all(isinstance(p, list) and len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= v <= 100 for p in points for v in p), "0 <= xi, yi <= 100"
