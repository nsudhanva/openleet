"""Maximum Number of Visible Points: integer points, a field-of-view angle and a location."""


def check(points: list[list[int]], angle: int, location: list[int]) -> None:
    assert 1 <= len(points) <= 10**5, "1 <= points.length <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert len(location) == 2, "location.length == 2"
    assert 0 <= angle < 360, "0 <= angle < 360"
    assert 0 <= location[0] <= 100 and 0 <= location[1] <= 100, "0 <= posx, posy <= 100"
    assert all(0 <= x <= 100 and 0 <= y <= 100 for x, y in points), "0 <= xi, yi <= 100"
