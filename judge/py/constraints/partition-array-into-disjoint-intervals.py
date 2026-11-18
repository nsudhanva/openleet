"""Partition Array into Disjoint Intervals: an integer array that can be split."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**6 for v in nums), "0 <= nums[i] <= 10^6"
    suffix_min = nums[:]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(suffix_min[i], suffix_min[i + 1])
    best = nums[0]
    for i in range(1, n):
        if best <= suffix_min[i]:
            return
        best = max(best, nums[i])
    raise AssertionError("there is at least one valid answer")
