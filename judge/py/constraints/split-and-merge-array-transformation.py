"""Split and Merge Array Transformation: two arrays where nums2 is a permutation of nums1."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert 2 <= n <= 6, "2 <= n <= 6"
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert all(-(10**5) <= v <= 10**5 for v in nums1 + nums2), "-10^5 <= nums1[i], nums2[i] <= 10^5"
    assert sorted(nums1) == sorted(nums2), "nums2 is a permutation of nums1"
