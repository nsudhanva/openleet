"""Convert an Array Into a 2D Array With Conditions: values within 1..length."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(1 <= v <= len(nums) for v in nums), "1 <= nums[i] <= nums.length"
