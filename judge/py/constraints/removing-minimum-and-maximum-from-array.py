"""Removing Minimum and Maximum From Array: an array of distinct integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert len(set(nums)) == len(nums), "the integers in nums are distinct"
