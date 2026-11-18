"""Divide Array Into Arrays With Max Difference: integers, count a multiple of 3, and a limit k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert n % 3 == 0, "n is a multiple of 3"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
