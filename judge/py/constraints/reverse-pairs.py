"""Reverse Pairs: an array of 32-bit integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
