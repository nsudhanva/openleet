"""Smallest Missing Multiple of K: a list of integers and a positive k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= k <= 100, "1 <= k <= 100"
