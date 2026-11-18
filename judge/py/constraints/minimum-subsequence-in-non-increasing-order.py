"""Minimum Subsequence in Non-Increasing Order: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 500, "1 <= nums.length <= 500"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
