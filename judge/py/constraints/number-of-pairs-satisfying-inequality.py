"""Number of Pairs Satisfying Inequality: two equal-length integer arrays and a diff."""


def check(nums1: list[int], nums2: list[int], diff: int) -> None:
    n = len(nums1)
    assert n == len(nums2), "n == nums1.length == nums2.length"
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in nums1), "-10^4 <= nums1[i] <= 10^4"
    assert all(-(10**4) <= v <= 10**4 for v in nums2), "-10^4 <= nums2[i] <= 10^4"
    assert -(10**4) <= diff <= 10**4, "-10^4 <= diff <= 10^4"
