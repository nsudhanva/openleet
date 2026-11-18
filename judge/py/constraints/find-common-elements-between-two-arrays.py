"""Find Common Elements Between Two Arrays: two integer lists."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 100, "1 <= n <= 100"
    assert 1 <= len(nums2) <= 100, "1 <= m <= 100"
    assert all(1 <= x <= 100 for x in nums1 + nums2), "1 <= nums1[i], nums2[i] <= 100"
