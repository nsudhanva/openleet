"""Maximum Distance Between a Pair of Values: two non-increasing arrays."""

from itertools import pairwise


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= nums1.length <= 10^5"
    assert 1 <= len(nums2) <= 10**5, "1 <= nums2.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums1), "1 <= nums1[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums2), "1 <= nums2[j] <= 10^5"
    assert all(a >= b for a, b in pairwise(nums1)), "nums1 is non-increasing"
    assert all(a >= b for a, b in pairwise(nums2)), "nums2 is non-increasing"
