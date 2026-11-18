"""Longest Consecutive Sequence: an unsorted array of integers."""


def check(nums: list[int]) -> None:
    assert 0 <= len(nums) <= 10**5, "0 <= nums.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
