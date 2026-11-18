"""Minimum Skips to Arrive at Meeting On Time: road lengths, a speed and hours available."""


def check(dist: list[int], speed: int, hoursBefore: int) -> None:
    assert 1 <= len(dist) <= 1000, "1 <= n <= 1000"
    assert all(1 <= d <= 10**5 for d in dist), "1 <= dist[i] <= 10^5"
    assert 1 <= speed <= 10**6, "1 <= speed <= 10^6"
    assert 1 <= hoursBefore <= 10**7, "1 <= hoursBefore <= 10^7"
