"""Circular Array Loop: a circular array of non-zero jumps."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5000, "1 <= nums.length <= 5000"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
    assert all(v != 0 for v in nums), "nums[i] != 0"
