"""Largest Component Size by Common Factor: an array of unique positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert len(set(nums)) == len(nums), "all the values of nums are unique"
