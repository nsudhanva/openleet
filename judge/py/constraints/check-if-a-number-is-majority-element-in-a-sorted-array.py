"""Check If a Number Is Majority Element in a Sorted Array: a sorted array and a target."""


def check(nums: list[int], target: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= target <= 10**9, "1 <= target <= 10^9"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in non-decreasing order"
    )
