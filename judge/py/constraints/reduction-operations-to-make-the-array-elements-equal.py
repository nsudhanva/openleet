"""Reduction Operations to Make the Array Elements Equal: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(1 <= v <= 5 * 10**4 for v in nums), "1 <= nums[i] <= 5 * 10^4"
