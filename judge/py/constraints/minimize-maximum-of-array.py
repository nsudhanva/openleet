"""Minimize Maximum of Array: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= n <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
