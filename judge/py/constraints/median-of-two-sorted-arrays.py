"""Median of Two Sorted Arrays: two sorted integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 0 <= len(nums1) <= 1000, "0 <= m <= 1000"
    assert 0 <= len(nums2) <= 1000, "0 <= n <= 1000"
    assert 1 <= len(nums1) + len(nums2) <= 2000, "1 <= m + n <= 2000"
    for a in (nums1, nums2):
        assert all(-(10**6) <= v <= 10**6 for v in a), "-10^6 <= nums[i] <= 10^6"
        assert all(a[i] <= a[i + 1] for i in range(len(a) - 1)), "arrays are sorted"
