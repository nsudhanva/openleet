"""Find the Difference of Two Arrays: two integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert isinstance(nums1, list) and isinstance(nums2, list), "nums1 and nums2 are arrays"
    assert 1 <= len(nums1) <= 1000, "1 <= nums1.length <= 1000"
    assert 1 <= len(nums2) <= 1000, "1 <= nums2.length <= 1000"
    assert all(-1000 <= v <= 1000 for v in nums1), "-1000 <= nums1[i] <= 1000"
    assert all(-1000 <= v <= 1000 for v in nums2), "-1000 <= nums2[i] <= 1000"
