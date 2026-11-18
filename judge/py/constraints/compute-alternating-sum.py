"""Compute Alternating Sum: an array of small positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= x <= 100 for x in nums), "1 <= nums[i] <= 100"
