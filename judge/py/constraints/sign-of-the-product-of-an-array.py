"""Sign of the Product of an Array: a list of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
