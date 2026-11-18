"""K Closest Points to Origin: a list of [x, y] points and k."""


def check(points: list[list[int]], k: int) -> None:
    assert 1 <= len(points) <= 10**4, "1 <= points.length <= 10^4"
    assert 1 <= k <= len(points), "1 <= k <= points.length"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**4) <= v <= 10**4 for p in points for v in p), "-10^4 <= xi, yi <= 10^4"
