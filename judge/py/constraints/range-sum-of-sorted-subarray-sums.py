"""Range Sum of Sorted Subarray Sums: nums, its length n and a 1-based range."""


def check(nums: list[int], n: int, left: int, right: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert n == len(nums), "n == nums.length"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= left <= right <= n * (n + 1) // 2, "1 <= left <= right <= n * (n + 1) / 2"
