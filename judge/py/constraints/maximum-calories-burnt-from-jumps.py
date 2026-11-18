"""Maximum Calories Burnt from Jumps: an array of heights."""


def check(heights: list[int]) -> None:
    assert 1 <= len(heights) <= 10**5, "1 <= n == heights.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in heights), "1 <= heights[i] <= 10^5"
