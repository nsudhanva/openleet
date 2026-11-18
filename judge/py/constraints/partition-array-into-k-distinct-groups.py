"""Partition Array Into K-Distinct Groups: an integer array and a group count k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert isinstance(k, int) and 1 <= k <= len(nums), "1 <= k <= nums.length"
