"""Tuple with Same Product: an array of distinct positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert len(set(nums)) == len(nums), "all elements in nums are distinct"
