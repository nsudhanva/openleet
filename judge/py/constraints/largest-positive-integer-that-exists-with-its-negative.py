"""Largest Positive Integer That Exists With Its Negative: an array of non-zero integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
    assert all(v != 0 for v in nums), "nums[i] != 0"
