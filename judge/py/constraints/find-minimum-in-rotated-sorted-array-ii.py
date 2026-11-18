"""Find Minimum in Rotated Sorted Array II: a sorted array, possibly with duplicates, rotated."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 5000, "1 <= n <= 5000"
    assert all(-5000 <= v <= 5000 for v in nums), "-5000 <= nums[i] <= 5000"
    drops = sum(nums[i] > nums[(i + 1) % n] for i in range(n))
    assert drops <= 1, "nums is sorted and rotated"
