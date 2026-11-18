"""Minimize Maximum Pair Sum in Array: an even-length list of positive integers."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert n % 2 == 0, "n is even"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
