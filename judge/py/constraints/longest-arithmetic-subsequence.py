"""Longest Arithmetic Subsequence: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 1500, "2 <= nums.length <= 1500"
    assert all(0 <= v <= 500 for v in nums), "0 <= nums[i] <= 500"
