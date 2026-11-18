"""Maximal Range That Each Element Is Maximum in It: an array of distinct positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert len(set(nums)) == len(nums), "all elements in nums are distinct"
