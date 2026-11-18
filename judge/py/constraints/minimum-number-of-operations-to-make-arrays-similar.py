"""Minimum Number of Operations to Make Arrays Similar: two equal-length integer arrays that
can be made similar."""


def check(nums: list[int], target: list[int]) -> None:
    assert isinstance(nums, list) and isinstance(target, list), "arrays"
    n = len(nums)
    assert n == len(target), "n == nums.length == target.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in target), "1 <= target[i] <= 10^6"
    assert sum(nums) == sum(target), "it is possible to make nums similar to target"
    assert sum(v % 2 for v in nums) == sum(v % 2 for v in target), (
        "it is possible to make nums similar to target"
    )
