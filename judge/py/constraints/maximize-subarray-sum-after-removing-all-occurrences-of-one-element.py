"""Maximize Subarray Sum After Removing All Occurrences of One Element: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**6) <= v <= 10**6 for v in nums), "-10^6 <= nums[i] <= 10^6"
