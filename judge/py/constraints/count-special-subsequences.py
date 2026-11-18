"""Count Special Subsequences: an integer array."""


def check(nums: list[int]) -> None:
    assert 7 <= len(nums) <= 1000, "7 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
