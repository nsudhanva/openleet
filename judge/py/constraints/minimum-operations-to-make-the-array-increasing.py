"""Minimum Operations to Make the Array Increasing: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 5000, "1 <= nums.length <= 5000"
    assert all(1 <= x <= 10**4 for x in nums), "1 <= nums[i] <= 10^4"
