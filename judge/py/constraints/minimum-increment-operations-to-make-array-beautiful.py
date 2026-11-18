"""Minimum Increment Operations to Make Array Beautiful: an integer array and a threshold k."""


def check(nums: list[int], k: int) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= n == nums.length <= 10^5"
    assert all(0 <= x <= 10**9 for x in nums), "0 <= nums[i] <= 10^9"
    assert 0 <= k <= 10**9, "0 <= k <= 10^9"
