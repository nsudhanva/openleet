"""Height Checker: a list of student heights."""


def check(heights: list[int]) -> None:
    assert 1 <= len(heights) <= 100, "1 <= heights.length <= 100"
    assert all(1 <= h <= 100 for h in heights), "1 <= heights[i] <= 100"
