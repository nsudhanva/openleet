"""Burst Balloons: balloon values."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 300, "1 <= n <= 300"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
