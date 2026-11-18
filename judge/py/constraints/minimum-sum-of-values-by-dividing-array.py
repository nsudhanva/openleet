"""Minimum Sum of Values by Dividing Array: nums and the AND values of its subarrays."""


def check(nums: list[int], andValues: list[int]) -> None:
    n, m = len(nums), len(andValues)
    assert 1 <= n <= 10**4, "1 <= n == nums.length <= 10^4"
    assert 1 <= m <= min(n, 10), "1 <= m == andValues.length <= min(n, 10)"
    assert all(1 <= v < 10**5 for v in nums), "1 <= nums[i] < 10^5"
    assert all(0 <= v < 10**5 for v in andValues), "0 <= andValues[j] < 10^5"
