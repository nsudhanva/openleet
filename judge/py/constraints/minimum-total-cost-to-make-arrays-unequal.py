"""Minimum Total Cost to Make Arrays Unequal: two equal-length arrays of values up to n."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert all(1 <= v <= n for v in nums1), "1 <= nums1[i] <= n"
    assert all(1 <= v <= n for v in nums2), "1 <= nums2[i] <= n"
