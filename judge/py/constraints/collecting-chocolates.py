"""Collecting Chocolates: chocolate costs and a rotation cost."""


def check(nums: list[int], x: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= x <= 10**9, "1 <= x <= 10^9"
