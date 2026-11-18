"""Unique Middle Element: an odd-length list of small positive integers."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 100, "1 <= nums.length <= 100"
    assert n % 2 == 1, "n is odd"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
