"""Minimum Absolute Difference Between Two Values: a short list of 0s, 1s and 2s."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(v in (0, 1, 2) for v in nums), "0 <= nums[i] <= 2"
