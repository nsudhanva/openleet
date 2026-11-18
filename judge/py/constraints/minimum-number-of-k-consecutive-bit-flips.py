"""Minimum Number of K Consecutive Bit Flips: a binary array and a flip length k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(v in (0, 1) for v in nums), "nums is a binary array"
    assert isinstance(k, int) and 1 <= k <= len(nums), "1 <= k <= nums.length"
