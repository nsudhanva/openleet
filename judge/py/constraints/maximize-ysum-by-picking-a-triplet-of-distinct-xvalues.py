"""Maximize Y-Sum by Picking a Triplet of Distinct X-Values: parallel lists x and y."""


def check(x: list[int], y: list[int]) -> None:
    n = len(x)
    assert len(y) == n, "n == x.length == y.length"
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert all(1 <= v <= 10**6 for v in x), "1 <= x[i] <= 10^6"
    assert all(1 <= v <= 10**6 for v in y), "1 <= y[i] <= 10^6"
