"""Kth Smallest Subarray Sum: positive integer array and a rank k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert all(1 <= v <= 5 * 10**4 for v in nums), "1 <= nums[i] <= 5 * 10^4"
    assert 1 <= k <= n * (n + 1) // 2, "1 <= k <= n * (n + 1) / 2"
