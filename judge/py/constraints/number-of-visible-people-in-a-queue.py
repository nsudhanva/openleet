"""Number of Visible People in a Queue: distinct heights."""


def check(heights: list[int]) -> None:
    assert isinstance(heights, list), "heights is a list"
    assert 1 <= len(heights) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= h <= 10**5 for h in heights), "1 <= heights[i] <= 10^5"
    assert len(set(heights)) == len(heights), "all the values of heights are unique"
