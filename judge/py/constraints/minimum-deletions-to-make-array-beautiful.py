"""Minimum Deletions to Make Array Beautiful: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= x <= 10**5 for x in nums), "0 <= nums[i] <= 10^5"
