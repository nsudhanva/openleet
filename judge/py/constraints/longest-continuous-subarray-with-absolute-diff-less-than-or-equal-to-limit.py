"""Longest Continuous Subarray With Absolute Diff <= Limit: an int array and a limit."""


def check(nums: list[int], limit: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= limit <= 10**9, "0 <= limit <= 10^9"
