"""Minimum Equal Sum of Two Arrays After Replacing Zeros: two non-negative integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= nums1.length <= 10^5"
    assert 1 <= len(nums2) <= 10**5, "1 <= nums2.length <= 10^5"
    assert all(0 <= x <= 10**6 for x in nums1), "0 <= nums1[i] <= 10^6"
    assert all(0 <= x <= 10**6 for x in nums2), "0 <= nums2[i] <= 10^6"
