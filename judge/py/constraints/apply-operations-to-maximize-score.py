"""Apply Operations to Maximize Score: positive integers and k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length == n <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= min(n * (n + 1) // 2, 10**9), "1 <= k <= min(n * (n + 1) / 2, 10^9)"
