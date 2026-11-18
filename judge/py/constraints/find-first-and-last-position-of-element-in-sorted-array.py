"""Find First and Last Position of Element in Sorted Array: a sorted integer list and a target."""

from itertools import pairwise


def check(nums: list[int], target: int) -> None:
    assert 0 <= len(nums) <= 10**5, "0 <= nums.length <= 10^5"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
    assert all(a <= b for a, b in pairwise(nums)), "nums is a non-decreasing array"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
