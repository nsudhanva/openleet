"""Minimum Distance Between Three Equal Elements I: an array with values in 1..n."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 100, "1 <= n == nums.length <= 100"
    assert all(1 <= x <= n for x in nums), "1 <= nums[i] <= n"
