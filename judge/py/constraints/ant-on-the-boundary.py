"""Ant on the Boundary: non-zero integer steps."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(-10 <= v <= 10 for v in nums), "-10 <= nums[i] <= 10"
    assert all(v != 0 for v in nums), "nums[i] != 0"
