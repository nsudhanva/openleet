"""Find the Number of Ways to Place People I: distinct 2D points."""


def check(points: list[list[int]]) -> None:
    assert 2 <= len(points) <= 50, "2 <= n <= 50"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= x <= 50 and 0 <= y <= 50 for x, y in points), (
        "0 <= points[i][0], points[i][1] <= 50"
    )
    assert len({tuple(p) for p in points}) == len(points), "All points[i] are distinct"
