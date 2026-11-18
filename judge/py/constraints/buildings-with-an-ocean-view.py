"""Buildings With an Ocean View: building heights."""


def check(heights: list[int]) -> None:
    assert 1 <= len(heights) <= 10**5, "1 <= heights.length <= 10^5"
    assert all(1 <= h <= 10**9 for h in heights), "1 <= heights[i] <= 10^9"
