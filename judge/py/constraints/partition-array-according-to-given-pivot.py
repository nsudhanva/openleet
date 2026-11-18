"""Partition Array According to Given Pivot: an integer array and a pivot taken from it."""


def check(nums: list[int], pivot: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**6) <= v <= 10**6 for v in nums), "-10^6 <= nums[i] <= 10^6"
    assert pivot in nums, "pivot equals an element of nums"
