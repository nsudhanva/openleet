"""Wiggle Sort: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(0 <= v <= 10**4 for v in nums), "0 <= nums[i] <= 10^4"
