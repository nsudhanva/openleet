"""Maximum Sum Circular Subarray: a circular integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= n <= 3 * 10^4"
    assert all(-3 * 10**4 <= v <= 3 * 10**4 for v in nums), "-3 * 10^4 <= nums[i] <= 3 * 10^4"
