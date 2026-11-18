"""Minimum Number of Taps to Open to Water a Garden: garden length n and tap ranges."""


def check(n: int, ranges: list[int]) -> None:
    assert isinstance(ranges, list), "ranges is a list"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert len(ranges) == n + 1, "ranges.length == n + 1"
    assert all(0 <= r <= 100 for r in ranges), "0 <= ranges[i] <= 100"
