"""Minimum Operations to Make Binary Array Elements Equal to One I: a binary array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(x in (0, 1) for x in nums), "0 <= nums[i] <= 1"
