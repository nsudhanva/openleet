"""Increasing Triplet Subsequence: a list of 32-bit integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**5, "1 <= nums.length <= 5 * 10^5"
    assert all(-(2**31) <= x <= 2**31 - 1 for x in nums), "-2^31 <= nums[i] <= 2^31 - 1"
