"""Construct Uniform Parity Array I: a list of distinct integers."""


def check(nums1: list[int]) -> None:
    assert isinstance(nums1, list), "nums1 is a list"
    assert 1 <= len(nums1) <= 100, "1 <= n == nums1.length <= 100"
    assert all(isinstance(v, int) for v in nums1), "nums1[i] is an integer"
    assert all(1 <= v <= 100 for v in nums1), "1 <= nums1[i] <= 100"
    assert len(set(nums1)) == len(nums1), "nums1 consists of distinct integers"
