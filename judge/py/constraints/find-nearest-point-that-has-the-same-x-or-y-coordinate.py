"""Find Nearest Point That Has the Same X or Y Coordinate: a location and a point list."""


def check(x: int, y: int, points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 10**4, "1 <= points.length <= 10^4"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert 1 <= x <= 10**4 and 1 <= y <= 10**4, "1 <= x, y <= 10^4"
    assert all(1 <= a <= 10**4 and 1 <= b <= 10**4 for a, b in points), "1 <= ai, bi <= 10^4"
