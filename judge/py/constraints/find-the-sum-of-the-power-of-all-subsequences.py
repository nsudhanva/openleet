"""Find the Sum of the Power of All Subsequences: an array and a target sum k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= n <= 100"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert 1 <= k <= 100, "1 <= k <= 100"
