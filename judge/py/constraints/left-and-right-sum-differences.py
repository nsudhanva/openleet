"""Left and Right Sum Differences: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
