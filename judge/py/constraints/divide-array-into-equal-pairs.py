"""Divide Array Into Equal Pairs: an array of 2 * n integers."""


def check(nums: list[int]) -> None:
    assert len(nums) % 2 == 0, "nums.length == 2 * n"
    assert 1 <= len(nums) // 2 <= 500, "1 <= n <= 500"
    assert all(1 <= v <= 500 for v in nums), "1 <= nums[i] <= 500"
