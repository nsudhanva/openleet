"""Chalkboard XOR Game: the numbers written on the board."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(isinstance(v, int) and 0 <= v < 2**16 for v in nums), "0 <= nums[i] < 2^16"
