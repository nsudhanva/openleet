"""Find the Array Concatenation Value: an integer array."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
