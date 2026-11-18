"""Minimum Right Shifts to Sort the Array: distinct small ints."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert len(set(nums)) == len(nums), "nums contains distinct integers"
