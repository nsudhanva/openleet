"""Find Anagram Mappings: two equal-length integer lists, the second an anagram of the first."""


def check(nums1: list[int], nums2: list[int]) -> None:
    assert 1 <= len(nums1) <= 100, "1 <= nums1.length <= 100"
    assert len(nums2) == len(nums1), "nums2.length == nums1.length"
    assert all(0 <= x <= 10**5 for x in nums1 + nums2), "0 <= nums1[i], nums2[i] <= 10^5"
    assert sorted(nums1) == sorted(nums2), "nums2 is an anagram of nums1"
