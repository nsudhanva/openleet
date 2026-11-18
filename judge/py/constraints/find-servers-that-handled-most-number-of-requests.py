"""Find Servers That Handled Most Number of Requests: k servers, arrival times and loads."""

from itertools import pairwise


def check(k: int, arrival: list[int], load: list[int]) -> None:
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert 1 <= len(arrival) <= 10**5, "1 <= arrival.length <= 10^5"
    assert len(arrival) == len(load), "arrival.length == load.length"
    assert all(1 <= a <= 10**9 for a in arrival), "1 <= arrival[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in load), "1 <= load[i] <= 10^9"
    assert all(a < b for a, b in pairwise(arrival)), "arrival is strictly increasing"
