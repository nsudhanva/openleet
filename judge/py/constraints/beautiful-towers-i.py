"""Beautiful Towers I: a list of maximum tower heights."""


def check(heights: list[int]) -> None:
    assert 1 <= len(heights) <= 10**3, "1 <= n == heights.length <= 10^3"
    assert all(1 <= h <= 10**9 for h in heights), "1 <= heights[i] <= 10^9"
