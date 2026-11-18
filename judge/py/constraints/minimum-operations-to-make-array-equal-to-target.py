"""Minimum Operations to Make Array Equal to Target: two positive integer lists, same length."""


def check(nums: list[int], target: list[int]) -> None:
    assert isinstance(nums, list) and isinstance(target, list), "nums and target are lists"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert len(nums) == len(target), "nums.length == target.length"
    assert all(1 <= x <= 10**8 for x in nums), "1 <= nums[i] <= 10^8"
    assert all(1 <= x <= 10**8 for x in target), "1 <= target[i] <= 10^8"
