"""4Sum II: four integer lists of equal length."""


def check(nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]) -> None:
    n = len(nums1)
    assert len(nums2) == len(nums3) == len(nums4) == n, "all four lists have length n"
    assert 1 <= n <= 200, "1 <= n <= 200"
    lim = 2**28
    for arr in (nums1, nums2, nums3, nums4):
        assert all(-lim <= x <= lim for x in arr), "-2^28 <= nums[i] <= 2^28"
