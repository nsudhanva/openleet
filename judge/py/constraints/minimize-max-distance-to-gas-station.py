"""Minimize Max Distance to Gas Station: sorted station positions and a count k."""

from itertools import pairwise


def check(stations: list[int], k: int) -> None:
    assert 10 <= len(stations) <= 2000, "10 <= stations.length <= 2000"
    assert all(0 <= v <= 10**8 for v in stations), "0 <= stations[i] <= 10^8"
    assert all(a < b for a, b in pairwise(stations)), (
        "stations is sorted in strictly increasing order"
    )
    assert 1 <= k <= 10**6, "1 <= k <= 10^6"
