"""Minimum Number of Arrows to Burst Balloons: [xstart, xend] balloon spans."""


def check(points: list[list[int]]) -> None:
    assert 1 <= len(points) <= 10**5, "1 <= points.length <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(2**31) <= s < e <= 2**31 - 1 for s, e in points), (
        "-2^31 <= xstart < xend <= 2^31 - 1"
    )
