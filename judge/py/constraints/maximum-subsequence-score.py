"""Maximum Subsequence Score: two equal-length non-negative arrays and a size k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    n = len(nums1)
    assert len(nums2) == n, "n == nums1.length == nums2.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums1), "0 <= nums1[i] <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums2), "0 <= nums2[j] <= 10^5"
    assert 1 <= k <= n, "1 <= k <= n"
