"""Limit Occurrences in Sorted Array: a sorted array and a limit k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert all(nums[i] <= nums[i + 1] for i in range(n - 1)), (
        "nums is sorted in non-decreasing order"
    )
    assert 1 <= k <= n, "1 <= k <= nums.length"
