"""Transformed Array: a circular integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(-100 <= x <= 100 for x in nums), "-100 <= nums[i] <= 100"
