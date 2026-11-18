"""Maximum Length of Repeated Subarray: two integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 1000, "1 <= nums1.length <= 1000"
    assert 1 <= len(nums2) <= 1000, "1 <= nums2.length <= 1000"
    assert all(0 <= v <= 100 for v in nums1), "0 <= nums1[i] <= 100"
    assert all(0 <= v <= 100 for v in nums2), "0 <= nums2[i] <= 100"
