"""Sum of All Subset XOR Totals: a short array of small positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 12, "1 <= nums.length <= 12"
    assert all(1 <= x <= 20 for x in nums), "1 <= nums[i] <= 20"
