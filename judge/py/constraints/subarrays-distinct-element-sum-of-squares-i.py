"""Subarrays Distinct Element Sum of Squares I: a short list of positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
