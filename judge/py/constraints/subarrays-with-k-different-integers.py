"""Subarrays with K Different Integers: values and k, both in 1..nums.length."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    n = len(nums)
    assert 1 <= n <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(isinstance(v, int) and 1 <= v <= n for v in nums), "1 <= nums[i] <= nums.length"
    assert isinstance(k, int) and 1 <= k <= n, "1 <= k <= nums.length"
