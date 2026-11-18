"""Sort Integers by Binary Reflection: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
