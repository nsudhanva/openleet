"""Count Complete Subarrays in an Array: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 2000 for v in nums), "1 <= nums[i] <= 2000"
