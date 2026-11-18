"""Max Dot Product of Two Subsequences: two integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 500, "1 <= nums1.length <= 500"
    assert 1 <= len(nums2) <= 500, "1 <= nums2.length <= 500"
    assert all(-1000 <= v <= 1000 for v in nums1), "-1000 <= nums1[i] <= 1000"
    assert all(-1000 <= v <= 1000 for v in nums2), "-1000 <= nums2[i] <= 1000"
