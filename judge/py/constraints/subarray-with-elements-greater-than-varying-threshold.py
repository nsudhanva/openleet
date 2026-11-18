"""Subarray With Elements Greater Than Varying Threshold: positive integers and a threshold."""


def check(nums: list[int], threshold: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert isinstance(threshold, int) and 1 <= threshold <= 10**9, "1 <= threshold <= 10^9"
