"""Kth Smallest Product of Two Sorted Arrays: two sorted integer arrays and a rank k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    assert 1 <= len(nums1) <= 5 * 10**4, "1 <= nums1.length <= 5 * 10^4"
    assert 1 <= len(nums2) <= 5 * 10**4, "1 <= nums2.length <= 5 * 10^4"
    assert all(-(10**5) <= v <= 10**5 for v in nums1), "-10^5 <= nums1[i] <= 10^5"
    assert all(-(10**5) <= v <= 10**5 for v in nums2), "-10^5 <= nums2[j] <= 10^5"
    assert 1 <= k <= len(nums1) * len(nums2), "1 <= k <= nums1.length * nums2.length"
    assert nums1 == sorted(nums1), "nums1 is sorted"
    assert nums2 == sorted(nums2), "nums2 is sorted"
