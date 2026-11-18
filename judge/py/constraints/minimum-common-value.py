"""Minimum Common Value: two sorted lists of positive integers."""

from itertools import pairwise


def check(nums1: list[int], nums2: list[int]) -> None:
    for name, a in (("nums1", nums1), ("nums2", nums2)):
        assert 1 <= len(a) <= 10**5, f"1 <= {name}.length <= 10^5"
        assert all(1 <= v <= 10**9 for v in a), f"1 <= {name}[i] <= 10^9"
        assert all(x <= y for x, y in pairwise(a)), f"{name} is sorted in non-decreasing order"
