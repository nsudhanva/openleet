"""Divide an Array Into Subarrays With Minimum Cost I: a list of small integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 50, "3 <= n <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
