"""Count Special Quadruplets: a short integer array."""


def check(nums: list[int]) -> None:
    assert 4 <= len(nums) <= 50, "4 <= nums.length <= 50"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
