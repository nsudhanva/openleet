"""Longest Even Odd Subarray With Threshold: an int array and a threshold."""


def check(nums: list[int], threshold: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= threshold <= 100, "1 <= threshold <= 100"
