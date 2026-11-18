"""Count Number of Rectangles Containing Each Point: [length, height] rectangles and points."""


def check(rectangles: list[list[int]], points: list[list[int]]) -> None:
    assert 1 <= len(rectangles) <= 5 * 10**4, "1 <= rectangles.length <= 5 * 10^4"
    assert 1 <= len(points) <= 5 * 10**4, "1 <= points.length <= 5 * 10^4"
    assert all(len(r) == 2 for r in rectangles), "rectangles[i].length == 2"
    assert all(len(p) == 2 for p in points), "points[j].length == 2"
    assert all(1 <= ln <= 10**9 and 1 <= h <= 100 for ln, h in rectangles), (
        "1 <= li <= 10^9, 1 <= hi <= 100"
    )
    assert all(1 <= x <= 10**9 and 1 <= y <= 100 for x, y in points), (
        "1 <= xj <= 10^9, 1 <= yj <= 100"
    )
    assert len({(ln, h) for ln, h in rectangles}) == len(rectangles), "all rectangles are unique"
    assert len({(x, y) for x, y in points}) == len(points), "all points are unique"
