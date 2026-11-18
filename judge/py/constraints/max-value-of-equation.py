"""Max Value of Equation: points sorted by strictly increasing x, and a distance bound."""


def check(points: list[list[int]], k: int) -> None:
    assert 2 <= len(points) <= 10**5, "2 <= points.length <= 10^5"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**8) <= c <= 10**8 for p in points for c in p), "-10^8 <= xi, yi <= 10^8"
    assert 0 <= k <= 2 * 10**8, "0 <= k <= 2 * 10^8"
    assert all(points[i][0] < points[i + 1][0] for i in range(len(points) - 1)), (
        "xi form a strictly increasing sequence"
    )
