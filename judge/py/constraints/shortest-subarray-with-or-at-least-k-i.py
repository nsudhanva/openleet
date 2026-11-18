"""Shortest Subarray With OR at Least K I: a short array of small non-negative integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(0 <= x <= 50 for x in nums), "0 <= nums[i] <= 50"
    assert 0 <= k < 64, "0 <= k < 64"
