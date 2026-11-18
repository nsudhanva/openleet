"""Smallest Index With Equal Value: a list of digits."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 9 for v in nums), "0 <= nums[i] <= 9"
