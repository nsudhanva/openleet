"""Minimum Swaps To Make Sequences Increasing: two equal-length integer arrays."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 2 <= len(nums1) <= 10**5, "2 <= nums1.length <= 10^5"
    assert len(nums2) == len(nums1), "nums2.length == nums1.length"
    assert all(0 <= v <= 2 * 10**5 for v in nums1), "0 <= nums1[i] <= 2 * 10^5"
    assert all(0 <= v <= 2 * 10**5 for v in nums2), "0 <= nums2[i] <= 2 * 10^5"
    # always possible: some keep/swap choice per index makes both arrays strictly increasing
    keep = swap = True
    for i in range(1, len(nums1)):
        a, b, c, d = nums1[i - 1], nums2[i - 1], nums1[i], nums2[i]
        new_keep = (keep and a < c and b < d) or (swap and b < c and a < d)
        new_swap = (swap and b < d and a < c) or (keep and a < d and b < c)
        keep, swap = new_keep, new_swap
    assert keep or swap, "the input always makes it possible"
