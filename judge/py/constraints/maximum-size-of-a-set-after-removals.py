"""Maximum Size of a Set After Removals: two equal-even-length integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    n = len(nums1)
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert n % 2 == 0, "n is even"
    assert all(1 <= v <= 10**9 for v in nums1), "1 <= nums1[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in nums2), "1 <= nums2[i] <= 10^9"
