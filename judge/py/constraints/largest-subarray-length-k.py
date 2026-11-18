"""Largest Subarray Length K: an array of distinct positive integers and a length k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "nums.length <= 10^5"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert len(set(nums)) == len(nums), "all the integers of nums are unique"
