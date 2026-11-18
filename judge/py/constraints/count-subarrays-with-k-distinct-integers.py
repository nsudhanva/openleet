"""Count Subarrays With K Distinct Integers: an integer array with k and m."""


def check(nums: list[int], k: int, m: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= k <= n, "1 <= k <= nums.length"
    assert 1 <= m <= n, "1 <= m <= nums.length"
