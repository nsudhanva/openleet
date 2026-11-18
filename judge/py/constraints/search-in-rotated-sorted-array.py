"""Search in Rotated Sorted Array: distinct integers, an ascending array possibly rotated, plus
a target."""


def check(nums: list[int], target: int) -> None:
    n = len(nums)
    assert 1 <= n <= 5000, "1 <= nums.length <= 5000"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert len(set(nums)) == n, "all values of nums are unique"
    assert -(10**4) <= target <= 10**4, "-10^4 <= target <= 10^4"
    drops = sum(nums[i] > nums[(i + 1) % n] for i in range(n))
    assert drops <= 1, "nums is an ascending array that is possibly rotated"
