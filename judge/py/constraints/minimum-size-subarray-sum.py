"""Minimum Size Subarray Sum: a target and an array of positive ints."""


def check(target: int, nums: list[int]) -> None:
    assert 1 <= target <= 10**9, "1 <= target <= 10^9"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
