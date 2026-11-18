"""Longest Subsequence With Decreasing Adjacent Difference: a list of integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**4, "2 <= nums.length <= 10^4"
    assert all(1 <= v <= 300 for v in nums), "1 <= nums[i] <= 300"
