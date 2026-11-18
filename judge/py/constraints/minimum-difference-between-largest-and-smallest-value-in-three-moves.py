"""Minimum Difference Between Largest and Smallest Value in Three Moves: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
