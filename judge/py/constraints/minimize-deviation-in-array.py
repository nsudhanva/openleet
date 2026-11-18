"""Minimize Deviation in Array: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
