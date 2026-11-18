"""Minimum Adjacent Swaps for K Consecutive Ones: a 0/1 list and a count k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(v in (0, 1) for v in nums), "nums[i] is 0 or 1"
    assert 1 <= k <= sum(nums), "1 <= k <= sum(nums)"
