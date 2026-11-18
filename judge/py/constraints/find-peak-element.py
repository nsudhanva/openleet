"""Find Peak Element: an integer array with no equal neighbours."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
    assert all(a != b for a, b in pairwise(nums)), "nums[i] != nums[i + 1] for all valid i"
