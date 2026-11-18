"""Find K Pairs with Smallest Sums: two sorted arrays and a pair count k."""


def check(nums1: list[int], nums2: list[int], k: int) -> None:
    assert 1 <= len(nums1) <= 10**5, "1 <= nums1.length <= 10^5"
    assert 1 <= len(nums2) <= 10**5, "1 <= nums2.length <= 10^5"
    for name, nums in (("nums1", nums1), ("nums2", nums2)):
        assert all(-(10**9) <= v <= 10**9 for v in nums), f"-10^9 <= {name}[i] <= 10^9"
        assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
            f"{name} is sorted in non-decreasing order"
        )
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
    assert k <= len(nums1) * len(nums2), "k <= nums1.length * nums2.length"
