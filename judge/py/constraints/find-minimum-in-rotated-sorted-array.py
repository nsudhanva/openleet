"""Find Minimum in Rotated Sorted Array: a sorted array of unique integers, rotated."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 5000, "1 <= n <= 5000"
    assert all(-5000 <= v <= 5000 for v in nums), "-5000 <= nums[i] <= 5000"
    assert len(set(nums)) == n, "all the integers of nums are unique"
    drops = sum(nums[i] > nums[(i + 1) % n] for i in range(n))
    assert drops <= 1, "nums is sorted and rotated"
