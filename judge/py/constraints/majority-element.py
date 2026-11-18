"""Majority Element: an array that has a value occurring more than n/2 times."""

from collections import Counter


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert max(Counter(nums).values()) > n // 2, "a majority element exists"
