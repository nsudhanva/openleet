"""Maximize the Minimum Powered City: station counts per city, range r, new stations k."""


def check(stations: list[int], r: int, k: int) -> None:
    n = len(stations)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**5 for v in stations), "0 <= stations[i] <= 10^5"
    assert 0 <= r <= n - 1, "0 <= r <= n - 1"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
