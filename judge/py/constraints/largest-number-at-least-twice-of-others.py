"""Largest Number At Least Twice of Others: a small array with a unique maximum."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 50, "2 <= nums.length <= 50"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
    assert nums.count(max(nums)) == 1, "the largest element in nums is unique"
