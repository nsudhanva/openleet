"""Minimum Operations to Make Array Non Decreasing: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
