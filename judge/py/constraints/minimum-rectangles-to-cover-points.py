"""Minimum Rectangles to Cover Points: distinct 2D points and a rectangle width w."""


def check(points: list[list[int]], w: int) -> None:
    assert 1 <= len(points) <= 10**5, "1 <= points.length <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(0 <= p[0] <= 10**9 for p in points), "0 <= xi <= 10^9"
    assert all(0 <= p[1] <= 10**9 for p in points), "0 <= yi <= 10^9"
    assert 0 <= w <= 10**9, "0 <= w <= 10^9"
    assert len({(p[0], p[1]) for p in points}) == len(points), "all pairs (xi, yi) are distinct"
