"""Find Target Indices After Sorting Array: an integer array and a target."""


def check(nums: list[int], target: int) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= target <= 100, "1 <= target <= 100"
