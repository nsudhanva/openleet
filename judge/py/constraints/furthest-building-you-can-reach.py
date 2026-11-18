"""Furthest Building You Can Reach: building heights, bricks and ladders."""


def check(heights: list[int], bricks: int, ladders: int) -> None:
    assert 1 <= len(heights) <= 10**5, "1 <= heights.length <= 10^5"
    assert all(1 <= h <= 10**6 for h in heights), "1 <= heights[i] <= 10^6"
    assert 0 <= bricks <= 10**9, "0 <= bricks <= 10^9"
    assert 0 <= ladders <= len(heights), "0 <= ladders <= heights.length"
