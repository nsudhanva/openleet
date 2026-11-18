"""Maximum Number of Operations With the Same Score II: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2000, "2 <= nums.length <= 2000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
