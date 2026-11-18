"""Sum of Subsequence Widths: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100000, "1 <= nums.length <= 100000"
    assert all(1 <= v <= 100000 for v in nums), "1 <= nums[i] <= 10^5"
