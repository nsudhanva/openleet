"""Longest Continuous Increasing Subsequence: an unsorted array of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
