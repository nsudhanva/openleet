"""Subsequence of Size K With the Largest Even Sum: an integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= x <= 10**5 for x in nums), "0 <= nums[i] <= 10^5"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
