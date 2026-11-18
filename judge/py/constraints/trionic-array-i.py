"""Trionic Array I: an integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 100, "3 <= n <= 100"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
