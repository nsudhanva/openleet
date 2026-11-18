"""Find the Number of Good Pairs II: two arrays of positive integers and a multiplier k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(nums2) <= 10**5, "1 <= m <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums1), "1 <= nums1[i] <= 10^6"
    assert all(1 <= v <= 10**6 for v in nums2), "1 <= nums2[j] <= 10^6"
    assert 1 <= k <= 10**3, "1 <= k <= 10^3"
