"""Remove One Element to Make the Array Strictly Increasing: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 2 <= len(nums) <= 1000, "2 <= nums.length <= 1000"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
