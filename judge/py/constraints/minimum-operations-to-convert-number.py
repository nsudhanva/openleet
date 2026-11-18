"""Minimum Operations to Convert Number: distinct integers, a start value and a goal."""


def check(nums: list[int], start: int, goal: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-(10**9) <= x <= 10**9 for x in nums), "-10^9 <= nums[i] <= 10^9"
    assert -(10**9) <= goal <= 10**9, "-10^9 <= goal <= 10^9"
    assert 0 <= start <= 1000, "0 <= start <= 1000"
    assert start != goal, "start != goal"
    assert len(set(nums)) == len(nums), "all the integers in nums are distinct"
