"""Next Greater Element I: nums1 is a subset of the distinct values of nums2."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= len(nums2) <= 1000, "1 <= nums1.length <= nums2.length <= 1000"
    assert all(0 <= v <= 10**4 for v in nums1 + nums2), "0 <= nums1[i], nums2[i] <= 10^4"
    assert len(set(nums1)) == len(nums1), "all integers in nums1 are unique"
    assert len(set(nums2)) == len(nums2), "all integers in nums2 are unique"
    assert set(nums1) <= set(nums2), "all the integers of nums1 also appear in nums2"
