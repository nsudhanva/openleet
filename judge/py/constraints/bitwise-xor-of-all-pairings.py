"""Bitwise XOR of All Pairings: two arrays of non-negative integers."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= nums1.length <= 10^5"
    assert 1 <= len(nums2) <= 10**5, "1 <= nums2.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in nums1), "0 <= nums1[i] <= 10^9"
    assert all(0 <= v <= 10**9 for v in nums2), "0 <= nums2[j] <= 10^9"
