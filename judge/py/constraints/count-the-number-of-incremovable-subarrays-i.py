"""Count the Number of Incremovable Subarrays I: an array of small positive integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 50, "1 <= nums.length <= 50"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
