"""Rotate Function: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
