"""Largest Sum of Averages: an array of positive integers and a group count k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert 1 <= k <= len(nums), "1 <= k <= nums.length"
