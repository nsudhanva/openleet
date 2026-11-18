"""Maximum Difference Between Adjacent Elements in a Circular Array: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
