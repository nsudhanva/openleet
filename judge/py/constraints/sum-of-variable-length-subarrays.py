"""Sum of Variable Length Subarrays: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
