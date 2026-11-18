"""Pour Water: terrain heights, a water volume and a drop index."""


def check(heights: list[int], volume: int, k: int) -> None:
    assert 1 <= len(heights) <= 100, "1 <= heights.length <= 100"
    assert all(0 <= h <= 99 for h in heights), "0 <= heights[i] <= 99"
    assert 0 <= volume <= 2000, "0 <= volume <= 2000"
    assert 0 <= k < len(heights), "0 <= k < heights.length"
