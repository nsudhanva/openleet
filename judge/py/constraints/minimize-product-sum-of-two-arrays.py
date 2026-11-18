"""Minimize Product Sum of Two Arrays: two equal-length lists of integers in 1..100."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert len(nums1) == len(nums2), "n == nums1.length == nums2.length"
    assert 1 <= len(nums1) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 100 for v in nums1), "1 <= nums1[i] <= 100"
    assert all(1 <= v <= 100 for v in nums2), "1 <= nums2[i] <= 100"
