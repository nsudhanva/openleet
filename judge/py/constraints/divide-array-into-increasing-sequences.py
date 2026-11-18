"""Divide Array Into Increasing Sequences: a sorted integer array and a length k."""

from itertools import pairwise


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 10**5, "1 <= k <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert all(a <= b for a, b in pairwise(nums)), "nums is sorted in non-decreasing order"
