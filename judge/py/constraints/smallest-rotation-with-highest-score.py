"""Smallest Rotation with Highest Score: values in [0, n)."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v < len(nums) for v in nums), "0 <= nums[i] < nums.length"
