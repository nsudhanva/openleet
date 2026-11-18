"""Eliminate Maximum Number of Monsters: monster distances and speeds."""


def check(dist: list[int], speed: list[int]) -> None:
    n = len(dist)
    assert len(speed) == n, "n == dist.length == speed.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in dist), "1 <= dist[i] <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in speed), "1 <= speed[i] <= 10^5"
