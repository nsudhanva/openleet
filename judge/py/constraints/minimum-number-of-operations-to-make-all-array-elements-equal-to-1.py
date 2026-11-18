"""Minimum Number of Operations to Make All Array Elements Equal to 1: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 2 <= len(nums) <= 50, "2 <= nums.length <= 50"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
