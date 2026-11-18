"""Count Hills and Valleys in an Array: a list of small positive integers."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 100, "3 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
