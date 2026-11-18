"""Smallest Missing Integer Greater Than Sequential Prefix Sum: a short list of small integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
