"""Maximum Count of Positive Integer and Negative Integer: a sorted integer array."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= nums.length <= 2000"
    assert all(-2000 <= v <= 2000 for v in nums), "-2000 <= nums[i] <= 2000"
    assert all(a <= b for a, b in pairwise(nums)), "nums is sorted in non-decreasing order"
