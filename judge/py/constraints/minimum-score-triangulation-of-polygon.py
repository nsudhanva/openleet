"""Minimum Score Triangulation of Polygon: vertex values of a convex polygon."""


def check(values: list[int]) -> None:
    assert 3 <= len(values) <= 50, "3 <= n <= 50"
    assert all(1 <= v <= 100 for v in values), "1 <= values[i] <= 100"
