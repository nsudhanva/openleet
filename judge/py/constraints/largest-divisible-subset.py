"""Largest Divisible Subset: an array of distinct positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 2 * 10**9 for v in nums), "1 <= nums[i] <= 2 * 10^9"
    assert len(set(nums)) == len(nums), "all the integers in nums are unique"
