"""Maximize Subarray GCD Score: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 1500, "1 <= n == nums.length <= 1500"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= n, "1 <= k <= n"
