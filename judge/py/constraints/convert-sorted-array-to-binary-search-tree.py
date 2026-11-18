"""Convert Sorted Array to Binary Search Tree: a strictly increasing list."""

from itertools import pairwise


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert all(a < b for a, b in pairwise(nums)), "nums is sorted in a strictly increasing order"
