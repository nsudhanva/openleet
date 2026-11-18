"""Widest Pair of Indices With Equal Range Sum: two equal-length binary arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(v in (0, 1) for v in nums1), "nums1[i] is either 0 or 1"
    assert all(v in (0, 1) for v in nums2), "nums2[i] is either 0 or 1"
