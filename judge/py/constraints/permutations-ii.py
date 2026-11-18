"""Permutations II: a list of integers, possibly with duplicates."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 8, "1 <= nums.length <= 8"
    assert all(-10 <= v <= 10 for v in nums), "-10 <= nums[i] <= 10"
