"""Maximum Total Subarray Value II: an array of non-negative ints and a count k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert 1 <= k <= min(10**5, n * (n + 1) // 2), "1 <= k <= min(10^5, n * (n + 1) / 2)"
