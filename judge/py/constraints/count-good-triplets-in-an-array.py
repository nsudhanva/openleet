"""Count Good Triplets in an Array: two permutations of 0..n-1."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert sorted(nums1) == list(range(n)), "nums1 is a permutation of [0, n - 1]"
    assert sorted(nums2) == list(range(n)), "nums2 is a permutation of [0, n - 1]"
