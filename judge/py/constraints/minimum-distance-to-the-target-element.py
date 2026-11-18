"""Minimum Distance to the Target Element: an array, a target present in it and a start index."""


def check(nums: list[int], target: int, start: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= x <= 10**4 for x in nums), "1 <= nums[i] <= 10^4"
    assert 0 <= start < len(nums), "0 <= start < nums.length"
    assert target in nums, "target is in nums"
