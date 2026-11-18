"""Maximum Number of Points with Cost: an m x n matrix of points."""


def check(points: list[list[int]]) -> None:
    m = len(points)
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    n = len(points[0])
    assert all(len(row) == n for row in points), "n == points[r].length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= m * n <= 10**5, "1 <= m * n <= 10^5"
    assert all(0 <= v <= 10**5 for row in points for v in row), "0 <= points[r][c] <= 10^5"
