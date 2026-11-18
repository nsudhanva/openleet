"""Minimum Sum of Mountain Triplets I: a short list of small positive integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 50, "3 <= nums.length <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
