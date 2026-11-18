"""Number of Longest Increasing Subsequence: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= nums.length <= 2000"
    assert all(-(10**6) <= v <= 10**6 for v in nums), "-10^6 <= nums[i] <= 10^6"
