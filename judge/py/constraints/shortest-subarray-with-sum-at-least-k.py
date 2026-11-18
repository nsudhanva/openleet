"""Shortest Subarray with Sum at Least K: an integer array and a positive k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**5) <= x <= 10**5 for x in nums), "-10^5 <= nums[i] <= 10^5"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
