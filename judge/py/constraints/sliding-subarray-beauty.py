"""Sliding Subarray Beauty: integers with window size k and rank x."""


def check(nums: list[int], k: int, x: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= k <= n, "1 <= k <= n"
    assert 1 <= x <= k, "1 <= x <= k"
    assert all(-50 <= v <= 50 for v in nums), "-50 <= nums[i] <= 50"
