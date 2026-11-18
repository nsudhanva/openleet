"""Shortest Subarray With OR at Least K II: an array of non-negative integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 2 * 10**5, "1 <= nums.length <= 2 * 10^5"
    assert all(0 <= x <= 10**9 for x in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
