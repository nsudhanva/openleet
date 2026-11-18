"""Maximize Sum Of Array After K Negations: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
