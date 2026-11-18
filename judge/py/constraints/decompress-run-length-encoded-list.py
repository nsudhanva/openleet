"""Decompress Run-Length Encoded List: a list of (frequency, value) pairs, flattened."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert len(nums) % 2 == 0, "nums.length % 2 == 0"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
