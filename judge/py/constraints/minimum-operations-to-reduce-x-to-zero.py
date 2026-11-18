"""Minimum Operations to Reduce X to Zero: an array of positive ints and a target x."""


def check(nums: list[int], x: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert 1 <= x <= 10**9, "1 <= x <= 10^9"
