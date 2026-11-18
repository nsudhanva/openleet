"""Continuous Subarray Sum: a list of non-negative integers and a divisor k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= sum(nums) <= 2**31 - 1, "0 <= sum(nums[i]) <= 2^31 - 1"
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= 2**31 - 1, "1 <= k <= 2^31 - 1"
