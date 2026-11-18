"""Longest Increasing Subsequence: an int array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2500, "1 <= nums.length <= 2500"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
