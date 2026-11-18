"""Triples with Bitwise AND Equal To Zero: an array of 16-bit integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(0 <= v < 2**16 for v in nums), "0 <= nums[i] < 2^16"
