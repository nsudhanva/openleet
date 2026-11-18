"""Min Cost to Connect All Points: distinct [x, y] points."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 1000, "1 <= points.length <= 1000"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**6) <= v <= 10**6 for p in points for v in p), "-10^6 <= xi, yi <= 10^6"
    assert len({tuple(p) for p in points}) == len(points), "all pairs (xi, yi) are distinct"
