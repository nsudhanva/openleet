"""Minimum Incompatibility: an array of at most 16 values and a subset count k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= k <= n <= 16, "1 <= k <= nums.length <= 16"
    assert n % k == 0, "nums.length is divisible by k"
    assert all(1 <= x <= n for x in nums), "1 <= nums[i] <= nums.length"
