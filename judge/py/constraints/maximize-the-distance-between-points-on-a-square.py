"""Maximize the Distance Between Points on a Square: side, unique boundary points, k."""


def check(side: int, points: list[list[int]], k: int) -> None:
    assert 1 <= side <= 10**9, "1 <= side <= 10^9"
    assert 4 <= len(points) <= min(4 * side, 15 * 10**3), (
        "4 <= points.length <= min(4 * side, 15 * 10^3)"
    )
    assert all(len(p) == 2 for p in points), "points[i] == [xi, yi]"
    assert all(0 <= x <= side and 0 <= y <= side for x, y in points), "points[i] lies in the square"
    assert all(x in (0, side) or y in (0, side) for x, y in points), (
        "points[i] lies on the boundary of the square"
    )
    assert len({(x, y) for x, y in points}) == len(points), "All points[i] are unique"
    assert 4 <= k <= min(25, len(points)), "4 <= k <= min(25, points.length)"
