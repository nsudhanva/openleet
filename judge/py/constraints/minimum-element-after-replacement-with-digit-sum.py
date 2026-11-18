"""Minimum Element After Replacement With Digit Sum: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= x <= 10**4 for x in nums), "1 <= nums[i] <= 10^4"
