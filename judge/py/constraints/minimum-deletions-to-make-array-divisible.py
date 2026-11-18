"""Minimum Deletions to Make Array Divisible: two positive integer arrays."""


def check(nums: list[int], numsDivide: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= len(numsDivide) <= 10**5, "1 <= numsDivide.length <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
    assert all(1 <= x <= 10**9 for x in numsDivide), "1 <= numsDivide[i] <= 10^9"
