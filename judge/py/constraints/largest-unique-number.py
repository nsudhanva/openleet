"""Largest Unique Number: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= nums.length <= 2000"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
