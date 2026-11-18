"""Maximum Number of Intersections on the Chart: y-coordinates of a line chart."""


def check(y: list[int]) -> None:
    assert 2 <= len(y) <= 10**5, "2 <= y.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in y), "1 <= y[i] <= 10^9"
    assert all(y[i] != y[i + 1] for i in range(len(y) - 1)), "y[i] != y[i + 1]"
