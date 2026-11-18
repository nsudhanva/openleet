"""Sum of Subarray Ranges: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
