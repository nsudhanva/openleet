"""Uncrossed Lines: two integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 500 and 1 <= len(nums2) <= 500, (
        "1 <= nums1.length, nums2.length <= 500"
    )
    assert all(1 <= v <= 2000 for v in nums1 + nums2), "1 <= nums1[i], nums2[j] <= 2000"
