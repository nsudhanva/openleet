"""Maximum XOR for Each Query: a sorted array of maximumBit-bit values and maximumBit."""

from itertools import pairwise


def check(nums: list[int], maximumBit: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= maximumBit <= 20, "1 <= maximumBit <= 20"
    assert all(0 <= v < 2**maximumBit for v in nums), "0 <= nums[i] < 2^maximumBit"
    assert all(a <= b for a, b in pairwise(nums)), "nums is sorted in ascending order"
