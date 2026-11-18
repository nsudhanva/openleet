"""Closest Subsequence Sum: an array and a goal."""


def check(nums: list[int], goal: int) -> None:
    assert 1 <= len(nums) <= 40, "1 <= nums.length <= 40"
    assert all(-(10**7) <= v <= 10**7 for v in nums), "-10^7 <= nums[i] <= 10^7"
    assert -(10**9) <= goal <= 10**9, "-10^9 <= goal <= 10^9"
