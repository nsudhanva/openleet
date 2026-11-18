"""Maximum Area Rectangle With Point Constraints I: a list of unique [x, y] points."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 10, "1 <= points.length <= 10"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= v <= 100 for p in points for v in p), "0 <= xi, yi <= 100"
    assert len({tuple(p) for p in points}) == len(points), "all points are unique"
