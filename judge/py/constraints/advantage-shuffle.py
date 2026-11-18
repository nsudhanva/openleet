"""Advantage Shuffle: two equal-length lists of non-negative integers."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= nums1.length <= 10^5"
    assert len(nums2) == len(nums1), "nums2.length == nums1.length"
    assert all(0 <= x <= 10**9 for x in nums1), "0 <= nums1[i] <= 10^9"
    assert all(0 <= x <= 10**9 for x in nums2), "0 <= nums2[i] <= 10^9"
