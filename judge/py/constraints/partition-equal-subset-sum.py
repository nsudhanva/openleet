"""Partition Equal Subset Sum: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
