"""Intersection of Two Arrays II: two arrays of integers in 0..1000."""


def check(nums1: list[int], nums2: list[int]) -> None:
    for a in (nums1, nums2):
        assert isinstance(a, list), "nums are lists"
        assert 1 <= len(a) <= 1000, "1 <= nums.length <= 1000"
        assert all(0 <= v <= 1000 for v in a), "0 <= nums[i] <= 1000"
