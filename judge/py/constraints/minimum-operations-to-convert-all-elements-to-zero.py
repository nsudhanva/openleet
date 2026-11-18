"""Minimum Operations to Convert All Elements to Zero: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(0 <= x <= 10**5 for x in nums), "0 <= nums[i] <= 10^5"
