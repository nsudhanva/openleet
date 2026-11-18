"""Teemo Attacking: sorted attack times and a poison duration."""

from itertools import pairwise


def check(timeSeries: list[int], duration: int) -> None:
    assert 1 <= len(timeSeries) <= 10**4, "1 <= timeSeries.length <= 10^4"
    assert all(0 <= t <= 10**7 for t in timeSeries), "0 <= timeSeries[i] <= 10^7"
    assert 0 <= duration <= 10**7, "0 <= duration <= 10^7"
    assert all(a <= b for a, b in pairwise(timeSeries)), (
        "timeSeries is sorted in non-decreasing order"
    )
