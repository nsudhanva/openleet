"""Subsets II: an array of integers that may repeat."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10, "1 <= nums.length <= 10"
    assert all(-10 <= x <= 10 for x in nums), "-10 <= nums[i] <= 10"
