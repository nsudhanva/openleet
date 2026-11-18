"""Frequency Balance Subarray: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**3, "1 <= nums.length <= 10^3"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
