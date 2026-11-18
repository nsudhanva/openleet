"""Smallest Range II: non-negative integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(0 <= v <= 10**4 for v in nums), "0 <= nums[i] <= 10^4"
    assert 0 <= k <= 10**4, "0 <= k <= 10^4"
