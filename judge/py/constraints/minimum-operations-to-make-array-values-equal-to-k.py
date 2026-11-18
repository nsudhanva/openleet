"""Minimum Operations to Make Array Values Equal to K: positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= x <= 100 for x in nums), "1 <= nums[i] <= 100"
    assert 1 <= k <= 100, "1 <= k <= 100"
