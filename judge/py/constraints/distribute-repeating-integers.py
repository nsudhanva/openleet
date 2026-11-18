"""Distribute Repeating Integers: an integer array with few distinct values and order quantities."""


def check(nums: list[int], quantity: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert 1 <= len(quantity) <= 10, "1 <= m <= 10"
    assert all(1 <= q <= 10**5 for q in quantity), "1 <= quantity[i] <= 10^5"
    assert len(set(nums)) <= 50, "at most 50 unique values in nums"
