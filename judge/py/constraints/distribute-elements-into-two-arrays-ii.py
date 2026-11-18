"""Distribute Elements Into Two Arrays II: a list of integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= n <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
