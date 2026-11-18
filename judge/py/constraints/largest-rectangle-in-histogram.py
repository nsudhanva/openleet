"""Largest Rectangle in Histogram: an array of bar heights."""


def check(heights: list[int]) -> None:
    assert 1 <= len(heights) <= 10**5, "1 <= heights.length <= 10^5"
    assert all(0 <= h <= 10**4 for h in heights), "0 <= heights[i] <= 10^4"
