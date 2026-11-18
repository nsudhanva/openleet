"""Smallest Index With Digit Sum Equal to Index: a list of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
