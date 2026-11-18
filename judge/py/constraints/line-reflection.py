"""Line Reflection: a list of 2D integer points."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 10**4, "1 <= n <= 10^4"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**8) <= v <= 10**8 for p in points for v in p), "-10^8 <= points[i][j] <= 10^8"
