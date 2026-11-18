"""Sort Array By Parity: a list of non-negative integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 5000, "1 <= nums.length <= 5000"
    assert all(isinstance(v, int) and 0 <= v <= 5000 for v in nums), "0 <= nums[i] <= 5000"
