"""Minimum Absolute Difference Between Elements With Constraint: integers and an index gap x."""


def check(nums: list[int], x: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 0 <= x < len(nums), "0 <= x < nums.length"
