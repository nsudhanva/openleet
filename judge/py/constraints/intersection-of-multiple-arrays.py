"""Intersection of Multiple Arrays: lists of distinct positive integers."""


def check(nums: list[list[int]]) -> None:
    assert isinstance(nums, list) and all(isinstance(a, list) for a in nums), "nums is a 2D list"
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert 1 <= sum(len(a) for a in nums) <= 1000, "1 <= sum(nums[i].length) <= 1000"
    for a in nums:
        assert all(1 <= v <= 1000 for v in a), "1 <= nums[i][j] <= 1000"
        assert len(set(a)) == len(a), "all the values of nums[i] are unique"
