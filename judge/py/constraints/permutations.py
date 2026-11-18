"""Permutations: a list of distinct integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 6, "1 <= nums.length <= 6"
    assert all(-10 <= v <= 10 for v in nums), "-10 <= nums[i] <= 10"
    assert len(set(nums)) == len(nums), "all the integers of nums are unique"
