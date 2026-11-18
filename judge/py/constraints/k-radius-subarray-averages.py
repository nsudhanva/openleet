"""K Radius Subarray Averages: a non-negative integer array and a radius k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert 0 <= k <= 10**5, "0 <= k <= 10^5"
