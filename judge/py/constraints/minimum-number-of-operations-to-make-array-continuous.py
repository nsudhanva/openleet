"""Minimum Number of Operations to Make Array Continuous: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
