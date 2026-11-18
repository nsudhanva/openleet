"""Longest Arithmetic Sequence After Changing At Most One Element: an integer array."""


def check(nums: list[int]) -> None:
    assert 4 <= len(nums) <= 10**5, "4 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
