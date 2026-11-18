"""Choose K Elements With Maximum Sum: two equal-length arrays and k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    n = len(nums1)
    assert n == len(nums2), "n == nums1.length == nums2.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**6 for v in nums1), "1 <= nums1[i] <= 10^6"
    assert all(1 <= v <= 10**6 for v in nums2), "1 <= nums2[i] <= 10^6"
    assert 1 <= k <= n, "1 <= k <= n"
