"""Partition Array Such That Maximum Difference Is K: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert isinstance(k, int) and 0 <= k <= 10**5, "0 <= k <= 10^5"
