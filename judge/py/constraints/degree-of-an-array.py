"""Degree of an Array: a non-empty array of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 50000, "1 <= nums.length <= 50000"
    assert all(0 <= v <= 49999 for v in nums), "0 <= nums[i] <= 49999"
