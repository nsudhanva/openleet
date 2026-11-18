"""Partition to K Equal Sum Subsets: an integer array and k."""

from collections import Counter


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert isinstance(k, int) and 1 <= k <= len(nums) <= 16, "1 <= k <= nums.length <= 16"
    assert all(isinstance(v, int) and 1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert all(1 <= c <= 4 for c in Counter(nums).values()), (
        "The frequency of each element is in the range [1, 4]"
    )
