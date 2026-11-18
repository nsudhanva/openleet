"""Non-decreasing Subsequences: a short array of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 15, "1 <= nums.length <= 15"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
