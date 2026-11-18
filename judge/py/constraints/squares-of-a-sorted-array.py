"""Squares of a Sorted Array: a sorted integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in non-decreasing order"
    )
