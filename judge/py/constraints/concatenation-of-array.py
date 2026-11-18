"""Concatenation of Array: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= n <= 1000"
    assert all(1 <= x <= 1000 for x in nums), "1 <= nums[i] <= 1000"
