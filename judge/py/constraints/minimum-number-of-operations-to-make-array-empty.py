"""Minimum Number of Operations to Make Array Empty: an array of positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
