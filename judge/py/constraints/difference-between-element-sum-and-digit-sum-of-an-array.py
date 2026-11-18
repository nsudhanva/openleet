"""Difference Between Element Sum and Digit Sum of an Array: positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= nums.length <= 2000"
    assert all(1 <= v <= 2000 for v in nums), "1 <= nums[i] <= 2000"
