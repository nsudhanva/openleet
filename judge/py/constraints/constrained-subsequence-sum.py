"""Constrained Subsequence Sum: an integer array and a window size k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 10**5, "1 <= k <= nums.length <= 10^5"
    assert all(-(10**4) <= x <= 10**4 for x in nums), "-10^4 <= nums[i] <= 10^4"
