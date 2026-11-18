"""Minimum Number of Refueling Stops: target distance, starting fuel and [position, fuel]
stations sorted by position."""

from itertools import pairwise


def check(target: int, startFuel: int, stations: list[list[int]]) -> None:
    assert isinstance(target, int) and 1 <= target <= 10**9, "1 <= target <= 10^9"
    assert isinstance(startFuel, int) and 1 <= startFuel <= 10**9, "1 <= startFuel <= 10^9"
    assert isinstance(stations, list) and 0 <= len(stations) <= 500, "0 <= stations.length <= 500"
    assert all(len(s) == 2 for s in stations), "stations[i].length == 2"
    assert all(1 <= p < target for p, _ in stations), "1 <= position_i < target"
    assert all(a[0] < b[0] for a, b in pairwise(stations)), "position_i < position_i+1"
    assert all(1 <= f < 10**9 for _, f in stations), "1 <= fuel_i < 10^9"
