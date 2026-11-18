"""Longest Non-decreasing Subarray From Two Arrays: two equal-length int arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert 1 <= n <= 10**5, "1 <= nums1.length <= 10^5"
    assert len(nums2) == n, "nums1.length == nums2.length == n"
    assert all(1 <= v <= 10**9 for v in nums1), "1 <= nums1[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in nums2), "1 <= nums2[i] <= 10^9"
