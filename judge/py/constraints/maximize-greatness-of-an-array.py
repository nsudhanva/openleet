"""Maximize Greatness of an Array: an array of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
