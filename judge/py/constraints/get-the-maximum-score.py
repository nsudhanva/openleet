"""Get the Maximum Score: two strictly increasing integer arrays."""

from itertools import pairwise


def check(nums1: list[int], nums2: list[int]) -> None:
    for name, nums in (("nums1", nums1), ("nums2", nums2)):
        assert 1 <= len(nums) <= 10**5, f"1 <= {name}.length <= 10^5"
        assert all(1 <= v <= 10**7 for v in nums), f"1 <= {name}[i] <= 10^7"
        assert all(a < b for a, b in pairwise(nums)), f"{name} is strictly increasing"
