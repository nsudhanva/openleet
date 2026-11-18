"""Longest Square Streak in an Array: a list of integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(2 <= v <= 10**5 for v in nums), "2 <= nums[i] <= 10^5"
