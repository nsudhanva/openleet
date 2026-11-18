"""Make Array Elements Equal to Zero: an array of 0..100 with at least one zero."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
    assert 0 in nums, "at least one element is 0"
