"""Number of Arithmetic Triplets: a strictly increasing array and a difference."""

from itertools import pairwise


def check(nums: list[int], diff: int) -> None:
    assert 3 <= len(nums) <= 200, "3 <= nums.length <= 200"
    assert all(0 <= v <= 200 for v in nums), "0 <= nums[i] <= 200"
    assert 1 <= diff <= 50, "1 <= diff <= 50"
    assert all(a < b for a, b in pairwise(nums)), "nums is strictly increasing"
