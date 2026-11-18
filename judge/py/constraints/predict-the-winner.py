"""Predict the Winner: a list of scores."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 20, "1 <= nums.length <= 20"
    assert all(0 <= v <= 10**7 for v in nums), "0 <= nums[i] <= 10^7"
