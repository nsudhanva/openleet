"""Largest Perimeter Triangle: an array of side lengths."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**4, "3 <= nums.length <= 10^4"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
