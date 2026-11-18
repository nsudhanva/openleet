"""Diagonal Traverse II: a jagged list of rows of integers."""


def check(nums: list[list[int]]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= len(r) <= 10**5 for r in nums), "1 <= nums[i].length <= 10^5"
    assert 1 <= sum(len(r) for r in nums) <= 10**5, "1 <= sum(nums[i].length) <= 10^5"
    assert all(1 <= v <= 10**5 for r in nums for v in r), "1 <= nums[i][j] <= 10^5"
