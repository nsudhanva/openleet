"""Minimum Elements to Add to Form a Given Sum: an array bounded by limit and a goal."""


def check(nums: list[int], limit: int, goal: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= limit <= 10**6, "1 <= limit <= 10^6"
    assert all(-limit <= x <= limit for x in nums), "-limit <= nums[i] <= limit"
    assert -(10**9) <= goal <= 10**9, "-10^9 <= goal <= 10^9"
