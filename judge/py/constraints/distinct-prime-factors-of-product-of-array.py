"""Distinct Prime Factors of Product of Array: integers between 2 and 1000."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(2 <= v <= 1000 for v in nums), "2 <= nums[i] <= 1000"
