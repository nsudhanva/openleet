"""Minimum Sum of Squared Difference: two equal-length arrays and two budgets."""


def check(nums1: list[int], nums2: list[int], k1: int, k2: int) -> None:
    n = len(nums1)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert all(0 <= v <= 10**5 for v in nums1), "0 <= nums1[i] <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums2), "0 <= nums2[i] <= 10^5"
    assert 0 <= k1 <= 10**9, "0 <= k1 <= 10^9"
    assert 0 <= k2 <= 10**9, "0 <= k2 <= 10^9"
