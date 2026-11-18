"""Sliding Window Median: 32-bit integers and a window size k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "nums.length <= 10^5"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in nums), "-2^31 <= nums[i] <= 2^31 - 1"
