"""Minimum Number of Operations to Make Elements in Array Distinct: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
