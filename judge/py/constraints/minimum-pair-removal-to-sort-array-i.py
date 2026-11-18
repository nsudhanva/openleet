"""Minimum Pair Removal to Sort Array I: a short array of ints."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
