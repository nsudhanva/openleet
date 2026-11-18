"""Smallest Stable Index I: non-negative integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
