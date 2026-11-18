"""Count Subarrays of Length Three With a Condition: an integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 100, "3 <= nums.length <= 100"
    assert all(-100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
