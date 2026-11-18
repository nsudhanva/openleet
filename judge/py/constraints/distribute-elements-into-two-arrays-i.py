"""Distribute Elements Into Two Arrays I: distinct integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 50, "3 <= n <= 50"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert len(set(nums)) == len(nums), "all elements in nums are distinct"
