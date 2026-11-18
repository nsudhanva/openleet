"""Construct Uniform Parity Array II: a list of distinct integers."""


def check(nums1: list[int]) -> None:
    assert isinstance(nums1, list), "nums1 is a list"
    assert 1 <= len(nums1) <= 10**5, "1 <= n == nums1.length <= 10^5"
    assert all(isinstance(v, int) for v in nums1), "nums1[i] is an integer"
    assert all(1 <= v <= 10**9 for v in nums1), "1 <= nums1[i] <= 10^9"
    assert len(set(nums1)) == len(nums1), "nums1 consists of distinct integers"
