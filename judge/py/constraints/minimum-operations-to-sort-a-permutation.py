"""Minimum Operations to Sort a Permutation: a permutation of 0..n-1."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(0 <= v <= n - 1 for v in nums), "0 <= nums[i] <= n - 1"
    assert len(set(nums)) == n, "nums is a permutation of integers from 0 to n - 1"
