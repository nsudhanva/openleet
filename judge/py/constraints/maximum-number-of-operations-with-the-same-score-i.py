"""Maximum Number of Operations With the Same Score I: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
