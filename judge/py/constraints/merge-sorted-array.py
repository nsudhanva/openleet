"""Merge Sorted Array: nums1 (m values then n zero slots), m, sorted nums2, n."""


def check(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    assert 0 <= m <= 200 and 0 <= n <= 200, "0 <= m, n <= 200"
    assert 1 <= m + n <= 200, "1 <= m + n <= 200"
    assert len(nums1) == m + n, "nums1.length == m + n"
    assert len(nums2) == n, "nums2.length == n"
    assert all(-(10**9) <= v <= 10**9 for v in nums1), "-10^9 <= nums1[i] <= 10^9"
    assert all(-(10**9) <= v <= 10**9 for v in nums2), "-10^9 <= nums2[j] <= 10^9"
    assert all(nums1[i] <= nums1[i + 1] for i in range(m - 1)), "nums1[:m] is sorted"
    assert all(v == 0 for v in nums1[m:]), "last n elements of nums1 are 0"
    assert all(nums2[i] <= nums2[i + 1] for i in range(n - 1)), "nums2 is sorted"
