"""Find Triangular Sum of an Array: an array of digits."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(0 <= v <= 9 for v in nums), "0 <= nums[i] <= 9"
