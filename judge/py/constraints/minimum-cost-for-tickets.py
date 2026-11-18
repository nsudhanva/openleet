"""Minimum Cost For Tickets: strictly increasing travel days and three ticket costs."""

from itertools import pairwise


def check(days: list[int], costs: list[int]) -> None:
    assert 1 <= len(days) <= 365, "1 <= days.length <= 365"
    assert all(1 <= d <= 365 for d in days), "1 <= days[i] <= 365"
    assert all(a < b for a, b in pairwise(days)), "days is in strictly increasing order"
    assert len(costs) == 3, "costs.length == 3"
    assert all(1 <= c <= 1000 for c in costs), "1 <= costs[i] <= 1000"
