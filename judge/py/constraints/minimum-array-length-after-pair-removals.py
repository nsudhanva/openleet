"""Minimum Array Length After Pair Removals: a sorted list of positive integers."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert all(a <= b for a, b in pairwise(nums)), "nums is sorted in non-decreasing order"
