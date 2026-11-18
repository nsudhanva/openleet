"""Final Array State After K Multiplication Operations I: nums, k and a multiplier."""


def check(nums: list[int], k: int, multiplier: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= x <= 100 for x in nums), "1 <= nums[i] <= 100"
    assert 1 <= k <= 10, "1 <= k <= 10"
    assert 1 <= multiplier <= 5, "1 <= multiplier <= 5"
