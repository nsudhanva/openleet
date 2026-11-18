"""Maximum Score Of Spliced Array: two equal-length positive integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**4 for v in nums1), "1 <= nums1[i] <= 10^4"
    assert all(1 <= v <= 10**4 for v in nums2), "1 <= nums2[i] <= 10^4"
