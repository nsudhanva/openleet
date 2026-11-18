"""Minimum Increase to Maximize Special Indices: an integer array of length at least 3."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= n <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
