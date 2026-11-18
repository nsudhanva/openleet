"""Find the Number of Ways to Place People II: a list of distinct [x, y] points."""


def check(points: list[list[int]]) -> None:
    n = len(points)
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert all(len(p) == 2 for p in points), "points[i].length == 2"
    assert all(-(10**9) <= v <= 10**9 for p in points for v in p), (
        "-10^9 <= points[i][0], points[i][1] <= 10^9"
    )
    assert len({tuple(p) for p in points}) == n, "all points[i] are distinct"
