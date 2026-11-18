"""Minimum Cost to Equalize Arrays Using Swaps: two equal-length integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert len(nums1) == len(nums2), "n == nums1.length == nums2.length"
    assert 2 <= len(nums1) <= 8 * 10**4, "2 <= n <= 8 * 10^4"
    assert all(1 <= x <= 8 * 10**4 for x in nums1), "1 <= nums1[i] <= 8 * 10^4"
    assert all(1 <= x <= 8 * 10**4 for x in nums2), "1 <= nums2[i] <= 8 * 10^4"
