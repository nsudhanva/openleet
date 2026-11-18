"""Create Maximum Number: digit arrays nums1 and nums2 and a target length k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    m, n = len(nums1), len(nums2)
    assert 1 <= m <= 500 and 1 <= n <= 500, "1 <= m, n <= 500"
    assert all(0 <= v <= 9 for v in nums1 + nums2), "0 <= nums1[i], nums2[i] <= 9"
    assert 1 <= k <= m + n, "1 <= k <= m + n"
    assert len(nums1) == 1 or nums1[0] != 0, "nums1 has no leading zeros"
    assert len(nums2) == 1 or nums2[0] != 0, "nums2 has no leading zeros"
