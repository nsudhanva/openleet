"""Minimum Index of a Valid Split: an integer array with exactly one dominant element."""

from collections import Counter


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
    top = Counter(nums).most_common(2)
    assert top[0][1] * 2 > len(nums), "nums has a dominant element"
    assert len(top) == 1 or top[1][1] * 2 <= len(nums), "exactly one dominant element"
