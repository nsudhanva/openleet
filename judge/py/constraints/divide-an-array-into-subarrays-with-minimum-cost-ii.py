"""Divide an Array Into Subarrays With Minimum Cost II: integers, a subarray count k and dist."""


def check(nums: list[int], k: int, dist: int) -> None:
    n = len(nums)
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 3 <= k <= n, "3 <= k <= n"
    assert k - 2 <= dist <= n - 2, "k - 2 <= dist <= n - 2"
