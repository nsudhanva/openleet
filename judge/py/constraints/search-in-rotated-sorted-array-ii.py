"""Search in Rotated Sorted Array II: a non-decreasing array rotated at some pivot, plus a
target."""


def check(nums: list[int], target: int) -> None:
    n = len(nums)
    assert 1 <= n <= 5000, "1 <= nums.length <= 5000"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert -(10**4) <= target <= 10**4, "-10^4 <= target <= 10^4"
    drops = sum(nums[i] > nums[(i + 1) % n] for i in range(n))
    assert drops <= 1, "nums is a non-decreasing array rotated at some pivot"
