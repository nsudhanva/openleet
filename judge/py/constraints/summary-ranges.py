"""Summary Ranges: a sorted array of unique integers."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    assert 0 <= len(nums) <= 20, "0 <= nums.length <= 20"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
    assert all(a < b for a, b in pairwise(nums)), "nums is sorted ascending with unique values"
