"""Choose Numbers From Two Arrays in Range: two equal-length arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert n == len(nums2), "n == nums1.length == nums2.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(0 <= v <= 100 for v in nums1), "0 <= nums1[i] <= 100"
    assert all(0 <= v <= 100 for v in nums2), "0 <= nums2[i] <= 100"
