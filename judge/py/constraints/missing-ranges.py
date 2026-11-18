"""Missing Ranges: a sorted unique array inside the inclusive range [lower, upper]."""

import itertools


def check(nums: list[int], lower: int, upper: int) -> None:
    assert -(10**9) <= lower <= upper <= 10**9, "-10^9 <= lower <= upper <= 10^9"
    assert 0 <= len(nums) <= 100, "0 <= nums.length <= 100"
    assert all(lower <= v <= upper for v in nums), "lower <= nums[i] <= upper"
    assert all(a < b for a, b in itertools.pairwise(nums)), "nums is sorted with unique values"
