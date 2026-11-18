"""Minimum Array Sum: non-negative integers with k and operation limits op1, op2."""


def check(nums: list[int], k: int, op1: int, op2: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert 0 <= k <= 10**5, "0 <= k <= 10^5"
    assert 0 <= op1 <= len(nums), "0 <= op1 <= nums.length"
    assert 0 <= op2 <= len(nums), "0 <= op2 <= nums.length"
