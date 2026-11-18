"""Reverse Subarray To Maximize Array Value: an array of integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 3 * 10**4, "2 <= nums.length <= 3 * 10^4"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
