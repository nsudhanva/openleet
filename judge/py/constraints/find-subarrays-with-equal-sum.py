"""Find Subarrays With Equal Sum: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 1000, "2 <= nums.length <= 1000"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
