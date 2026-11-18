"""Partition Array to Minimize XOR: an integer array and a group count k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 250, "1 <= nums.length <= 250"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert isinstance(k, int) and 1 <= k <= len(nums), "1 <= k <= n"
